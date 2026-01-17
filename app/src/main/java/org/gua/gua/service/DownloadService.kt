package org.gua.gua.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import org.gua.gua.R
import org.gua.gua.data.repository.GameRepository
import javax.inject.Inject

@AndroidEntryPoint
class DownloadService : Service() {
    
    @Inject
    lateinit var gameRepository: GameRepository
    
    private val serviceScope = CoroutineScope(Dispatchers.IO + Job())
    
    companion object {
        const val CHANNEL_ID = "DOWNLOAD_CHANNEL"
        const val NOTIFICATION_ID = 2001
        
        const val ACTION_START_DOWNLOAD = "START_DOWNLOAD"
        const val ACTION_STOP_DOWNLOAD = "STOP_DOWNLOAD"
        
        const val EXTRA_DOWNLOAD_TYPE = "download_type"
        const val DOWNLOAD_TYPE_GAME_IMAGES = "game_images"
        const val DOWNLOAD_TYPE_CACHE_UPDATE = "cache_update"
    }
    
    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START_DOWNLOAD -> {
                val downloadType = intent.getStringExtra(EXTRA_DOWNLOAD_TYPE)
                startForegroundService()
                startDownload(downloadType)
            }
            ACTION_STOP_DOWNLOAD -> {
                stopSelf()
            }
        }
        return START_NOT_STICKY
    }
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Downloads",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Background downloads and cache updates"
                setShowBadge(false)
            }
            
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }
    
    private fun startForegroundService() {
        val notification = createNotification("Preparing download...", 0)
        startForeground(NOTIFICATION_ID, notification)
    }
    
    private fun createNotification(text: String, progress: Int): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_gamepad)
            .setContentTitle("G.U.A Download")
            .setContentText(text)
            .setProgress(100, progress, progress == 0)
            .setOngoing(true)
            .setSilent(true)
            .build()
    }
    
    private fun startDownload(downloadType: String?) {
        serviceScope.launch {
            try {
                when (downloadType) {
                    DOWNLOAD_TYPE_GAME_IMAGES -> downloadGameImages()
                    DOWNLOAD_TYPE_CACHE_UPDATE -> updateCache()
                    else -> updateCache()
                }
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                stopSelf()
            }
        }
    }
    
    private suspend fun downloadGameImages() {
        updateNotification("Downloading game images...", 25)
        // Simulate download process
        kotlinx.coroutines.delay(2000)
        updateNotification("Processing images...", 75)
        kotlinx.coroutines.delay(1000)
        updateNotification("Download complete", 100)
    }
    
    private suspend fun updateCache() {
        updateNotification("Updating game cache...", 30)
        gameRepository.refreshCache()
        updateNotification("Cache updated", 100)
    }
    
    private fun updateNotification(text: String, progress: Int) {
        val notification = createNotification(text, progress)
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(NOTIFICATION_ID, notification)
    }
}