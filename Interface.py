import customtkinter
from ChatAPIClient import ChatAPIClient

standard_font = ("Roboto", 20)

class MainScreen(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("AI Chatbot")

        # Configure screen layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Create root frame to hold response boxes
        self.root_frame = customtkinter.CTkScrollableFrame(self)
        # Place it so it covers entire screen
        self.root_frame.grid(row=0, column=0, sticky="nesw")

        # Configure frame layout
        # Allows for placing response boxes
        self.root_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.root_frame.columnconfigure((0, 1), weight=1)

        # Input box for user to enter prompt
        self.prompt_input = customtkinter.CTkEntry(self,
                                                   height=70,
                                                   width=800,
                                                   placeholder_text="Input Prompt:",
                                                   font=standard_font)
        # Place input box at bottom of screen
        self.prompt_input.grid(row=1, column=0, pady=(20, 10))

        # Button for sending prompt
        self.send_prompt_button = customtkinter.CTkButton(self,
                                                          text="Send Prompt",
                                                          font=standard_font,
                                                          width=200,
                                                          height=50,
                                                          command=self.send_prompt)
        self.send_prompt_button.grid(row=2, column=0, pady=(10, 20))


        # Connect to API client
        self.chatbot = ChatAPIClient()

    # Method called when send prompt button is pressed
    def send_prompt(self):
        # Retrieve user's prompt from input box
        prompt = self.prompt_input.get()

        # Display the message in GUI
        self.display_message("You", prompt)

        # Clear the input box
        self.prompt_input.delete(0, "end")

        # Send the prompt to AWS and display the AI response
        self.get_ai_response(prompt)

    def get_ai_response(self, prompt):

        # Send message to API
        response = self.chatbot.send_api_request(prompt)

        # Display the response in GUI
        self.display_message("AI", response)


    def display_message(self, sender, text):
        # Format the message
        message_text = f"{sender}: {text}"

        message_textbox = customtkinter.CTkTextbox(self.root_frame,
                                                   width=700,
                                                   height=120,
                                                   font=standard_font)
        message_textbox.insert("1.0", message_text)

        # Find the first free row
        grid_free = False

        # AI responses start from second to top row and left side
        # User responses start from top row and right side

        if sender == "AI":
            current_row = 1
            sticky_setting="w"
            column = 0
        else:
            current_row = 0
            sticky_setting = "e"
            column = 1

        # Find the first free row

        grid_free = False

        # Check if current grid position is free
        while not grid_free:
            # If current grid position already has a message in
            if self.root_frame.grid_slaves(row=current_row, column=column):
                # Go down two rows
                current_row += 2
            else:
                # If it's free, insert message
                grid_free = True

        # Insert message into first free row
        message_textbox.grid(row=current_row,
                             column=column,
                             sticky=sticky_setting,
                             padx=(20, 20),
                             pady=(20, 20))



# Run the interface
main_screen = MainScreen()
main_screen.mainloop()

