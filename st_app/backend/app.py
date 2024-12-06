from flask import Flask, jsonify, request

import sys, os
# Add the 'models' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import RFV_Main
from models import LLM

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from EnvMgr import EnvManager



# Initialize Flask app
app = Flask(__name__)

# Flask routes: /analysis&category=<category>&productName=<productName>
@app.route('/analysis', methods=["GET"])
def get_analysis():

    category = request.args.get("category", "")
    productName = request.args.get("productName", "")
    print(f"Category: {category}\t productName: {productName}")

    data1 = RFV_Main.fetch_stats(productName, category, "azon"),
    data2 = RFV_Main.fetch_stats(productName, category, "fkart"),
    data1, data2 = data1[0], data2[0]
    stats = {
        "azon" : [data1['positive_count'], data1['neutral_count'], data1['negative_count']],
        "fkart": [data2['positive_count'], data2['neutral_count'], data2['negative_count']]
    }
    suggestions = caafr_llm.chat_caafr(stats, env_mgr.get_env_key("LLM_MODEL"))

    response = {
        "product_name": productName,
        "category": category,
        "azon": data1,
        "fkart": data2,
        "llm_suggestion": suggestions,
    }

    return jsonify(response)



# Run the Flask app
if __name__ == '__main__':

    # Initialize Dot-Env Manager
    env_mgr = EnvManager(".env")
    caafr_llm = LLM.CAAFR_LLM(env_mgr.get_env_key("LLM_API_KEY"))
    RFV_Main.install_packages()

    PORT = os.environ.get("PORT", int(env_mgr.get_env_key("BACKEND_PORT")))
    print(f"Back-end Server running @http://localhost:{PORT}")
    # app.run(debug=False, host="0.0.0.0", port=PORT)
    # app.run(debug=True, port=PORT)

    from werkzeug.serving import run_simple
    run_simple('localhost', PORT, app)
