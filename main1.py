from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd

pt = pickle.load(open(r"C:\\pt.pkl",'rb'))
amazon_data = pickle.load(open(r"C:\\items.pkl",'rb'))
similarity_scores = pickle.load(open(r"C:\\similarity_scores.pkl",'rb'))

app = Flask(__name__, template_folder='E:\\backup\\OneDrive\\Desktop\\Data Science\\Project\\Recommendation')

@app.route('/')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_items',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = amazon_data[amazon_data['productId'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('productId')['productId'].values))
        item.extend(list(temp_df.drop_duplicates('productId')['Rating'].values))
        item.extend(list(temp_df.drop_duplicates('productId')['link'].values))



        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
