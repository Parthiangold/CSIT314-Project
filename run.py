from app import createApp

# Invokes the createApp function which creates the localhost server for debug testing
app = createApp()

# Runs the localhost server 
if __name__ == "__main__":
    app.run(debug=True)
