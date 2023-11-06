import time
from os.path import join, dirname, realpath

from plyer import gps
from plyer import notification
from plyer.utils import platform
from plyer import vibrator

import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

kivy.require('1.8.0')


class Navigator(ScreenManager):
    pass


class HomePage(Screen):
    pass

# TODO 1: GPS with start button, pause if loc off and show dialogue box, display coord then stop


class DemoApp(MDApp):
    gps_location = StringProperty(defaultvalue="Getting Location")
    gps_status = StringProperty('Click Start to get GPS location updates')

    # def on_start(self):
    #     gps.configure(on_location=self.on_location)
    #
    # def on_location(self, **kwargs):
    #     self.gps_location = '\n'.join([
    #         '{}={}'.format(k, v) for k, v in kwargs.items()])


    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime. This function requests permission and handles the response via a callback.

        The request will produce a popup if permissions have not already been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        # def callback(permissions, results):
        #     """
        #     Defines the callback to be fired when runtime permission has been granted or denied. This is not strictly required, but added for the sake of completeness.
        #     """
        #     if all([res for res in results]):
        #         print("callback. All permissions granted.")
        #     else:
        #         print("callback. Some permissions refused.")

        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION], callback)
        # # To request permissions without a callback, do:
        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION])

    # def build(self):
    #     self.theme_cls.primary_palette = "Orange" # to set theme color for dialogue box
    #
    #     try:
    #         gps.configure(on_location=self.on_location,
    #                       on_status=self.on_status)
    #     except NotImplementedError:
    #         import traceback
    #         traceback.print_exc()
    #         self.gps_status = 'GPS is not implemented for your platform'
    #
    #     if platform == "android":
    #         print("gps.py: Android detected. Requesting permissions")
    #         self.request_android_permissions()
    #     main_kv = Builder.load_file("demo.kv")
    #     return main_kv

    def on_start(self):
        self.theme_cls.primary_palette = "Orange"  # to set theme color for dialogue box

        # try:
        gps.configure(on_location=self.on_location,
                      on_status=self.on_status)
        # except NotImplementedError:
        #     import traceback
        #     traceback.print_exc()
        #     self.gps_status = 'GPS is not implemented for your platform'

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

            while self.gps_location == "Getting Location":
                print("------------- GPS STARTING -------------")
                gps.start(1000, 0)
                print(f"--------- Co-ords - {self.gps_location} ---------")
            else:
                time.sleep(10)

                print("------------- GPS STOPPING -------------")
                gps.stop()
                print(f"--------- Final Co-ords - {self.gps_location} ---------")


        # ------------------- Build kv file -------------------
        main_kv = Builder.load_file("demo.kv")
        return main_kv

    # def start(self, minTime, minDistance):
    #     gps.start(minTime, minDistance)
    #     print("GPS STARTING")
    #     print(self.gps_location)
    #
    # def stop(self):
    #     gps.stop()
    #     print("GPS STOPPED")

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    @mainthread
    def on_status(self, stype, status):
        if status == 'provider-enabled':
            self.gps_status = 'type={}\n{}'.format(stype, status)
        else:
            self.open_gps_access_popup()

    # Popup to tell you to turn on location for app
    def open_gps_access_popup(self):
        self.on_pause()
        print("GPS ERROR")
        dialog = MDDialog(
                title="Location Error",
                text="App needs Location enabled to function properly",
                buttons=[MDFlatButton(text="OK"), ], )  # To add button in dialogue box
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()

    # def on_pause(self):
    #     gps.stop()
    #     return True
    #
    # def on_resume(self):
    #     print('Button Pressed, gps resuming')
    #     gps.start(1000, 0)
    #     pass


if __name__ == '__main__':
    DemoApp().run()









    #             NOT WORKING!!!
    # 1. DIALOG BOX OK NOT WORKING, TEST EXAMPLE ALONE (POP UP WHEN START BUTTON PRESSED)
    # 2. GPS NOT WORKING, REMOVE stop() FROM gps.start() FUNCTION
    # 3. GET GPS ON START OF APP (CHECK SANDBURG YOUTUBE VIDEO)












# TODO 2: Plyer Fancy notification with GPS coords
# TODO 3: Set alarm to send notification
# TODO 4: UI/UX logo, splash screen, name & loading animation