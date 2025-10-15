"""
AI Agent for Automatic Hotel Bookings
A mini project demonstrating an AI agent that helps users find and book hotels
"""

import os
from datetime import datetime, timedelta
from openai import OpenAI
import json

# Mock hotel database
HOTELS = [
    {
        "id": 1,
        "name": "Grand Plaza Hotel",
        "location": "New York",
        "price_per_night": 250,
        "rating": 4.5,
        "amenities": ["WiFi", "Pool", "Gym", "Restaurant"]
    },
    {
        "id": 2,
        "name": "Seaside Resort",
        "location": "Miami",
        "price_per_night": 180,
        "rating": 4.2,
        "amenities": ["WiFi", "Beach Access", "Spa"]
    },
    {
        "id": 3,
        "name": "Budget Inn",
        "location": "New York",
        "price_per_night": 80,
        "rating": 3.8,
        "amenities": ["WiFi", "Parking"]
    },
    {
        "id": 4,
        "name": "Luxury Suites",
        "location": "Los Angeles",
        "price_per_night": 350,
        "rating": 4.8,
        "amenities": ["WiFi", "Pool", "Gym", "Spa", "Restaurant", "Room Service"]
    }
]

# Mock bookings storage
bookings = []

def search_hotels(location, max_price=None, min_rating=None):
    """Search hotels based on criteria"""
    results = [h for h in HOTELS if h["location"].lower() == location.lower()]
    
    if max_price:
        results = [h for h in results if h["price_per_night"] <= max_price]
    
    if min_rating:
        results = [h for h in results if h["rating"] >= min_rating]
    
    return results

def book_hotel(hotel_id, guest_name, check_in, check_out, num_guests):
    """Book a hotel"""
    hotel = next((h for h in HOTELS if h["id"] == hotel_id), None)
    
    if not hotel:
        return {"success": False, "message": "Hotel not found"}
    
    # Calculate total price
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (check_out_date - check_in_date).days
    total_price = hotel["price_per_night"] * nights
    
    booking = {
        "booking_id": len(bookings) + 1,
        "hotel_name": hotel["name"],
        "guest_name": guest_name,
        "check_in": check_in,
        "check_out": check_out,
        "num_guests": num_guests,
        "nights": nights,
        "total_price": total_price
    }
    
    bookings.append(booking)
    
    return {
        "success": True,
        "booking": booking,
        "message": f"Booking confirmed! Total: ${total_price}"
    }

def get_booking_details(booking_id):
    """Get details of a booking"""
    booking = next((b for b in bookings if b["booking_id"] == booking_id), None)
    
    if not booking:
        return {"success": False, "message": "Booking not found"}
    
    return {"success": True, "booking": booking}

# Define tools for the AI agent
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": "Search for hotels based on location and optional filters",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City or location to search hotels"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price per night"
                    },
                    "min_rating": {
                        "type": "number",
                        "description": "Minimum rating (out of 5)"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_hotel",
            "description": "Book a hotel room",
            "parameters": {
                "type": "object",
                "properties": {
                    "hotel_id": {
                        "type": "integer",
                        "description": "ID of the hotel to book"
                    },
                    "guest_name": {
                        "type": "string",
                        "description": "Name of the guest"
                    },
                    "check_in": {
                        "type": "string",
                        "description": "Check-in date (YYYY-MM-DD)"
                    },
                    "check_out": {
                        "type": "string",
                        "description": "Check-out date (YYYY-MM-DD)"
                    },
                    "num_guests": {
                        "type": "integer",
                        "description": "Number of guests"
                    }
                },
                "required": ["hotel_id", "guest_name", "check_in", "check_out", "num_guests"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_booking_details",
            "description": "Retrieve details of an existing booking",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "integer",
                        "description": "ID of the booking"
                    }
                },
                "required": ["booking_id"]
            }
        }
    }
]

# Function mapping
available_functions = {
    "search_hotels": search_hotels,
    "book_hotel": book_hotel,
    "get_booking_details": get_booking_details
}

def run_agent(user_message, conversation_history=None):
    """Run the AI agent with function calling"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    if conversation_history is None:
        conversation_history = []
    
    # Add system message if starting new conversation
    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": "You are a helpful hotel booking assistant. Help users search for hotels and make bookings. Be friendly and confirm all booking details before finalizing."
        })
    
    # Add user message
    conversation_history.append({"role": "user", "content": user_message})
    
    # Call the API
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=conversation_history,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    conversation_history.append(response_message)
    
    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"\n🔧 Calling function: {function_name}")
            print(f"   Arguments: {function_args}")
            
            # Execute the function
            function_response = available_functions[function_name](**function_args)
            
            # Add function response to conversation
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(function_response)
            })
        
        # Get final response with function results
        final_response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=conversation_history
        )
        
        final_message = final_response.choices[0].message
        conversation_history.append(final_message)
        
        return final_message.content, conversation_history
    
    return response_message.content, conversation_history

def main():
    """Main interactive loop"""
    print("🏨 Hotel Booking AI Agent")
    print("=" * 50)
    print("Ask me to search hotels or make a booking!")
    print("Type 'quit' to exit\n")
    
    conversation_history = None
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Thank you for using the Hotel Booking Agent! Goodbye! 👋")
            break
        
        if not user_input:
            continue
        
        try:
            response, conversation_history = run_agent(user_input, conversation_history)
            print(f"\n🤖 Agent: {response}\n")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Please set OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your-key-here'")
    else:
        main()
