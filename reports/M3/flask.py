def render_photo_as_page(filename):
    """
    call predict.py, make predictions about uploaded images
    Each call copies the uploaded image to static"""
    img = Image.open(os.path.join(UPLOAD_FOLDER, filename))  #Upload folder and static are separated
    img.save(os.path.join('./static/images', filename)) 
    #predict
    preds = predict(filename)
    result = {}
    result["prediction"] = preds[0]
    result["probability"] = preds[1]
    result["fileName"] =  filename
    return result     

@app.route('/upload/<path:fileName>', methods=['POST', 'GET'])
def update(fileName):
    """Enter the URL to load the picture and return the predicted value; When you upload an image, it will be redirected here as well"""
    result = render_photo_as_page(fileName) 
    return render_template('show.html', fname='images/'+fileName, result=result) 
    #Pass the image path and prediction results to the front end
