def handle_error(error):
    response = {
        "success": False,
        "message": str(error)
    }
    return response, 400

def log_error(error):
    with open('error.log', 'a') as f:
        f.write(f"{error}\n")