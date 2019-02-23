from tornado.web import UIModule


class MyClass_01(UIModule):
    def render(self, *args, **kwargs):
        return 'ui_modules'



class Advertisement(UIModule):
    def render(self, *args, **kwargs):
        # UIModule中返回页面用render_string
        return self.render_string('ad_01.html')



    def javascript_files(self):
        return [
            'js/t_01.js',
        ]

    def css_files(self):
        return 'css/t_01.ss'