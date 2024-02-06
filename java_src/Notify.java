package org.test.myapp;
//The package name of your android app

import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.Context;
import android.os.Bundle;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import android.app.Notification;
import android.os.Build;
import android.media.RingtoneManager;
import android.net.Uri;
import android.media.AudioAttributes;
import org.test.myapp.R;
import java.lang.Math;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

public class Notify extends BroadcastReceiver {

    // This function is run when the BroadcastReceiver is fired
    @Override
    public void onReceive(Context context, Intent intent) {
        // function to create notification channel
        this.createNotificationChannel(context);
        // function to create the notification
        this.sendNotification(context, intent);

    }

    private void createNotificationChannel(Context context) {

        //checks if android version is equal to or above nougat else doesnt do anything
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            Uri sound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

            AudioAttributes att = new AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_NOTIFICATION)
                .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                .build();
            // Sets the name of the notification channel
            CharSequence name = "Scream";
            // sets the description of the notification channel
            String description = "Suncream Application Reminder";
            int importance = NotificationManager.IMPORTANCE_HIGH;
            NotificationChannel channel = new NotificationChannel("NOTIFICATION", name, importance);
            channel.setDescription(description);
            channel.setSound(sound, att);
            channel.enableLights(true);
            channel.enableVibration(true);
            NotificationManager notificationManager = context.getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);

            Log.i("python", "Notification Channel created");
        }
    }

    private void sendNotification(Context context, Intent intent) {
        Uri uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        //Bundle extras = new Bundle();
        Bundle extras = intent.getExtras();
        //String argument = extras.getString("reminderTask");
        String title = extras.getString("title");
        String content = extras.getString("content");
        String ticker = extras.getString("ticker");

        Log.i("python", title + ' ' + content + ' ' + ticker + ' ' );

	//try
	//{
	//	JSONObject jsonArgument = new JSONObject(argument);
	//	System.out.println("JSON Object: "+jsonArgument);
	//	Log.i("python", jsonArgument.toString());
	//}
	//catch (JSONException e)
	//{
	//	System.out.println("Error "+e.toString());
	//	Log.i("ERROR", e.toString());
	//}
        //String argument = getIntent().getStringExtra("reminderTask");
        //Intent intent = getIntent();

        //String argument = intent.getStringExtra("reminderTask");
        //Log.i("python", argument);


        //String title= "Reapply!!";
        //String content= "Stay Protected! Time to reapply your sunscreen.";
        //String ticker= "Screaaam";

        //create an unique notification id. Here it is done using random numbers
        int notification_id = (int)(Math.random() * (8000 - 1 + 1) + 1);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, "NOTIFICATION")
            .setSmallIcon(R.drawable.ic_launcher)
            .setContentTitle(title)
            .setContentText(content)
            .setTicker(ticker)
            .setSound(uri)
            .setAutoCancel(true)
            .setOnlyAlertOnce(false);

        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
        notificationManager.notify(notification_id, builder.build());
        Log.i("python", "Notification Sent");
    }
}
