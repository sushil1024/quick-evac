from twilio.rest import Client
from flask import current_app

class SMSService:
    """Service for sending SMS notifications using Twilio."""
    
    def __init__(self):
        """Initialize the Twilio client."""
        self.client = Client(
            current_app.config['TWILIO_ACCOUNT_SID'],
            current_app.config['TWILIO_AUTH_TOKEN']
        )
        self.from_number = current_app.config['TWILIO_PHONE_NUMBER']
    
    def send_evacuation_alert(self, to_number, zone_type, current_address, directions=None):
        """
        Send evacuation alert SMS to user.
        
        Args:
            to_number (str): Recipient phone number
            zone_type (str): Type of zone (RED, ORANGE, GREEN)
            current_address (str): User's current address
            directions (dict, optional): Directions to safe zone
            
        Returns:
            str: Message SID if sent successfully, None otherwise
        """
        try:
            # Format the message based on zone type
            if zone_type == 'RED':
                message_body = f"⚠️ EMERGENCY ALERT ⚠️\n\nYou are currently in a HIGH DANGER zone at: {current_address}. IMMEDIATE EVACUATION is required!"
                
                if directions:
                    message_body += f"\n\nEvacuation route ({directions['distance']}, {directions['duration']}):\n- Head to: {directions['end_address']}"
                    
                    # Add first 2-3 steps for immediate guidance
                    steps = directions['steps'][:3]  # Limit to first 3 steps
                    if steps:
                        message_body += "\n\nImmediate steps:"
                        for i, step in enumerate(steps, 1):
                            # Extract just the text from the HTML instructions
                            instruction = step['instruction'].replace('<b>', '').replace('</b>', '').replace('<div>', '\n').replace('</div>', '')
                            message_body += f"\n{i}. {instruction} ({step['distance']})"
                
                message_body += "\n\nStay calm and follow official evacuation routes. This is a QUICK EVAC emergency notification."
                
            elif zone_type == 'ORANGE':
                message_body = f"⚠️ WARNING ALERT ⚠️\n\nYou are in a MEDIUM DANGER zone at: {current_address}. Prepare for possible evacuation and stay alert for further instructions.\n\nThis is a QUICK EVAC notification."
                
            else:  # GREEN or unknown
                message_body = f"✓ SAFETY NOTIFICATION\n\nYou are currently in a SAFE zone at: {current_address}. No evacuation is necessary at this time.\n\nThis is a QUICK EVAC notification."
            
            # Send the message
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=to_number
            )
            
            current_app.logger.info(f"SMS sent to {to_number}: {message.sid}")
            return message.sid
            
        except Exception as e:
            current_app.logger.error(f"Error sending SMS: {str(e)}")
            return None