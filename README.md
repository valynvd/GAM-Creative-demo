
# GAM Creative Demo

A lightweight web application that demonstrates how to preview and test ad creatives integrated with Google Ad Manager (GAM).  
This project helps developers and ad-ops engineers visualize creative rendering and debug ad setup issues before deployment.

---

## Features

- Preview and test ad creatives dynamically
- Serve multiple ad sizes and formats (display, responsive, etc.)
- Supports asynchronous ad loading
- Frontend served on Vercel
- Built for ad tech engineers and publishers

---

## Tech Stack

- Backend: Python (Flask / FastAPI)
- Frontend: HTML, JavaScript
- Hosting: Vercel
- API Integration: Google Ad Manager API

---

## Installation

Clone the repository:

```bash
git clone https://github.com/valynvd/GAM-Creative-demo.git
cd GAM-Creative-demo
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Locally

Start the development server:

```bash
python app.py
```

Then open your browser and visit:

```
http://localhost:8000
```

If using Flask, you can also run:

```bash
flask run
```

---

## Deployment

This app is deployed on [Vercel](https://vercel.com/).
To deploy your own version:

1. Push your repository to GitHub.
2. Connect your GitHub repo to Vercel.
3. Set your build command and environment variables (if any).
4. Deploy directly from Vercel’s dashboard.

---

## Project Structure

```
GAM-Creative-demo/
├── app.py
├── static/
│   └── js/
│   └── css/
├── templates/
│   └── index.html
├── requirements.txt
├── vercel.json
└── README.md
```

---

## Example Usage

Visit the demo:
[https://gam-creative-demo.vercel.app/](https://gam-creative-demo.vercel.app/)

Example API request (if available):

```bash
curl -X GET http://localhost:8000/api/creative?id=12345
```

---

## Contributing

1. Fork the project
2. Create a new feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to your branch (`git push origin feature/my-feature`)
5. Submit a Pull Request

---

## License

This project is licensed under the MIT License.
See the `LICENSE` file for details.

---

## Author

Created by **[Valynvd](https://github.com/valynvd)**


```
