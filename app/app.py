import reflex as rx

def index():
    return rx.center(
        rx.vstack(
            rx.heading("Real-Time Scheduling Algorithm Simulator", size="lg"),
            rx.text("Select an algorithm and configure tasks to simulate."),
            spacing="4",
        ),
        height="100vh",
    )

app = rx.App()
app.add_page(index, route="/")