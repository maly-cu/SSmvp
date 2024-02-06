from os.path import join, dirname, realpath
from datetime import datetime, timedelta
#from geopy.geocoders import Nominatim
from jnius import autoclass, cast
import time
import json

from plyer import gps
from plyer import notification, vibrator
from plyer.utils import platform

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


class AppNotification(Screen):
    pass

# TODO 1: GPS with start button, pause if loc off and show dialogue box, display coord then stop


class DemoApp(MDApp):
    gps_location = StringProperty(defaultvalue="Getting Location")
    gps_status = StringProperty('Click Start to get GPS location updates')
    all_permissions_granted = False

    @mainthread
    def on_location(self, **kwargs):
        # self.gps_location = '\n'.join([
        #     '{}={}'.format(k, v) for k, v in kwargs.items()])
        self.gps_location = f"lat: {kwargs['lat']}, \nlon: {kwargs['lon']}"

    @mainthread
    def on_status(self, stype, status):
        if status == 'provider-enabled':
            self.gps_status = 'type={}\n{}'.format(stype, status)
        else:
            self.open_gps_access_popup()

    # Popup to tell you to turn on location for app
    def open_gps_access_popup(self):
        self.stop_gps(0)
        print("GPS ERROR")
        dialog = MDDialog(
                title="Location Error",
                text="Please turn on Location and restart app to use SunScream", )
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()

    def start_gps(self, dt):
        gps.start(1000, 0)
        print("------------- GPS STARTING -------------")
        print(f"--------- Co-ords - {self.gps_location} ---------")

    def stop_gps(self, dt):
        if self.gps_location != "Getting Location":
            print("------------- GPS STOPPING -------------")
            gps.stop()
            print(f"--------- Final Co-ords - {self.gps_location} ---------")

    def run_gps(self):
        print(f"--------- After permissions, waiting 2 seconds ---------")
        Clock.schedule_once(self.start_gps, 2)  # after 2 secs, start gps

        Clock.schedule_once(self.stop_gps, 12)  # after 9 secs, stop gps
        print(f"--------- After 9 seconds, coords - {self.gps_location} ---------")

    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime. This function requests permission and handles the response via a callback.
        The request will produce a popup if permissions have not already been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """ Defines the callback to be fired when runtime permission has been granted or denied.
            This is not strictly required, but added for the sake of completeness. """
            if all([res for res in results]):
                self.all_permissions_granted = True
                print(f"callback. All permissions granted.\nResults: {results}\nPermissions: {permissions}")
                print(f"All Permissions set to: {self.all_permissions_granted}")
                self.run_gps()
            else:
                print(f"callback. Some permissions refused.\nResults: {results}\nPermissions: {permissions}")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION,
                             Permission.INTERNET], callback)
        # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])

    def on_start(self):
        self.theme_cls.primary_palette = "Orange"  # to set theme color for dialogue box

        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")

            print(f"Permissions status: {self.all_permissions_granted}")
            self.request_android_permissions()

        # NOT WORKING, PYTHON COMPILING ALL AT ONCE. PUTTING IN CALLBACK FUNCTION
            # Check if all permissions have been granted then get location
            # if self.all_permissions_granted is True:
            # # DO THESE ONLY AFTER GETTING PERMISSIONS (i.e after they press allow)
            #
            # print(f"--------- After permissions, waiting 2 seconds ---------")
            # Clock.schedule_once(self.start_gps, 2)  # after 2 secs, start gps
            #
            # Clock.schedule_once(self.stop_gps, 9)  # after 9 secs, stop gps
            # print(f"--------- After 9 seconds, coords - {self.gps_location} ---------")

    # SINCE .kv file HAS SAME NAME AS APP, IT WILL RUN AUTOMATICALLY WITHOUT BUILD
    # FOR NOW, as build function is empty, no need for it.
    # def build(self):
    #     # ------------------- Build kv file -------------------
    #     main_kv = Builder.load_file("demo.kv")
    #     return main_kv

    # TODO 2: Plyer Fancy notification with GPS coords
    def schedule(self, *args):
        Clock.schedule_once(self.alarm, 1)  # after 2 secs, start alarm

    def alarm(self, *args):

        task_details = {'title': 'Screaaam', 'content': f'Reapply RIGHT NOW from {self.gps_location}', 'ticker': 'Heyyy!!'}
        task = json.dumps(task_details)
        print(f"Task: {task} of type {type(task)}")

        # Gets the current running instance of the app so as to speak
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity

        context = mActivity.getApplicationContext()
        Context = autoclass("android.content.Context")
        Intent = autoclass("android.content.Intent")
        # Bundle = autoclass("android.app.Bundle")
        Bundle = autoclass("android.os.Bundle")
        PendingIntent = autoclass("android.app.PendingIntent")
        String = autoclass("java.lang.String")
        Int = autoclass("java.lang.Integer")
        AlarmManager = autoclass('android.app.AlarmManager')
        Notify = autoclass('org.test.myapp.Notify')

        extras = Bundle()
        # extras.putString("reminderTask", task)
        extras.putString("title", task_details['title'])
        extras.putString("content", task_details['content'])
        extras.putString("ticker", task_details['ticker'])

        intent = Intent()
        intent.setClass(context, Notify)
        # Add additional data to the intent. The name must include a package prefix, for example the app com.android.contacts would use names like "com.android.contacts.ShowAll".

        intent.putExtras(extras)
        intent.setAction("org.test.myapp.NOTIFY")
        intent_id = 1

        pending_intent = PendingIntent.getBroadcast(
            context, intent_id, intent, PendingIntent.FLAG_CANCEL_CURRENT
        )

        ring_time = (time.time_ns() // 1_000_000) + 120_000
        print(f'Ring time is {ring_time} of type {type(ring_time)}')

        cast(
            AlarmManager, context.getSystemService(Context.ALARM_SERVICE)
        ).setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, ring_time, pending_intent)

        # # Get current time
        # current_time = datetime.now()
        #
        # # Calculating future time using timedelta()
        # # after two hours
        # set_time = current_time + timedelta(minutes=2)
        #
        # print(f'Reminder set at {current_time.time()}\b to go off at {set_time.time()}')
        #
        # while True:
        #     if set_time == datetime.now():
        #         self.do_notify()
        #         break

    # def do_notify(self):

        # title = 'Where are you??'
        # message = self.gps_location
        # ticker = 'ticker?'
        # app_name = 'SunScream'
        # app_icon = join(dirname(realpath(__file__)), 'plyer-icon.png')
        #
        # kwargs = {'app_name': app_name, 'app_icon': app_icon,
        #           'title': title, 'message': message, 'ticker': ticker}
        # notification.notify(**kwargs)

    # def get_location(self):
    #     location = [self.gps_location].raw[]
    #     """ Get state and country location from lat and lon"""
    #     # initialize Nominatim API
    #     geolocator = Nominatim(user_agent="geoapiExercises")
    #     # 4: Now get the information from the given list and parsed into a dictionary with raw function().
    #     self.map_location = geolocator.reverse(self.gps_location['lat'] + "," + self.gps_location['lon']).raw['address']

    # TODO 3: Set alarm to send notification


if __name__ == '__main__':
    DemoApp().run()



# TODO 4: UI/UX logo, splash screen, name & loading animation
