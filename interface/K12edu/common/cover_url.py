from random import choice


def get_cover_url():
    cover_url_list = ['https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/static/resource/%E6%AD%A3%E9%9D%A2.png',
                      'https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/static/resource/banner.png',
                      'https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/static/resource/WechatIMG1.png',
                      'https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/static/resource/'
                      '4f6cb54924a9b33561217b6038c18dc.jpg',
                      'https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/static/resource/1080about.png']
    cover_url = choice(cover_url_list)
    return cover_url

# print(cover_url())
