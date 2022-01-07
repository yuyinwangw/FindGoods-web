from tensorflow.keras import models
from tensorflow.keras.preprocessing import image
import os
import numpy as np
import app


def img_recognition(model, fname):
    net = models.load_model(model)
    cls_list = ['Cushion', 'desk', 'footstool', 'frame', 'lamps', 'mugs', 'vasesbowl']

    # 辨識一張圖
    # img = Image.open(os.path.join("C:/Users/TibeMe_user/Desktop/FindGoods-web/static/img/uploads/mugs.jpg"))
    img = image.load_img(os.path.join(app.config['default'].UPLOAD_FOLDER, fname), target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    pred = net.predict(x)[0]
    top_inds = pred.argsort()[::-1]
    list1 = []
    for i in top_inds:
        list2 = [pred[i], cls_list[i]]
        list1.append(list2)
    return list1


if __name__ == '__main__':
    # # 載入訓練好的模型
    #
    # net = models.load_model('model-resnet50-final.h5')
    # print(os.getcwd())
    # cls_list = ['Cushion', 'desk', 'footstool', 'frame', 'lamps', 'mugs', 'vasesbowl']
    # path1 = os.path.normpath(os.path.join(app.config['default'].UPLOAD_FOLDER, 'mugs.jpg'))
    #
    # # 辨識一張圖
    # # path = r'C:\Users\TibeMe_user\Desktop\FindGoods-web\app\static\img\uploads\mugs.jpg'
    # # os.path.join(app.config['default'].UPLOAD_FOLDER, 'mugs.jpg')
    # img = Image.open(os.path.join(app.config['default'].UPLOAD_FOLDER, 'mugs.jpg'))
    # # img = image.load_img(os.path.join(app.config['default'].UPLOAD_FOLDER, 'mugs.jpg'), target_size=(224, 224))
    # img = img.resize((224, 224))
    # plt.imshow(img)
    # plt.show()
    # x = image.img_to_array(img)
    # x = np.expand_dims(x, axis=0)
    # pred = net.predict(x)[0]
    # print(pred)
    # top_inds = pred.argsort()[::-1]
    # print(top_inds)
    # # print('    {:.3f}  {}'.format(pred[i], cls_list[i]))
    # pred_cls = {}
    # for i in top_inds:
    #     print('    {:.3f}  {}'.format(pred[i], cls_list[i]))
    path = os.getcwd()
    print(path)
    # new_path = path + "\\mugs.jpg"
    # new_path = new_path.replace("\\", "/")
    # img = image.load_img(new_path, target_size=(224, 224))
    # print(img)
    # img = image.load_img(os.path.join(app.config['default'].UPLOAD_FOLDER, 'mugs.jpg'), target_size=(224, 224))
    # namelist = img_recognition('mugs.jpg')
    # print(namelist)
