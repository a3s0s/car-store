from app import app

# This is the entry point for Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

# For Vercel serverless functions
application = app

if __name__ == "__main__":
    app.run()