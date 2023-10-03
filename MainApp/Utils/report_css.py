from weasyprint import HTML, CSS
from django.conf import settings

class report_css(object):
    
    @staticmethod
    def getCss():
        css_rapport = [
                
                CSS(settings.STATIC_ROOT +  '/css/report.css'),
            #CSS(settings.STATIC_ROOT +  '/css/bootstrap.css'),
                ]
        
        return css_rapport
    
    @staticmethod
    def getCssLandscape():
        css_rapport = [
                
                CSS(settings.STATIC_ROOT +  '/css/report_landscape.css'),
                #CSS(settings.STATIC_ROOT +  '/css/bootstrap.css'),
                ]
        
        return css_rapport