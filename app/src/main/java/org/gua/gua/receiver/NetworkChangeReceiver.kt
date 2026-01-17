package org.gua.gua.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.data.local.UserPreferences
import org.gua.gua.service.DownloadService
import javax.inject.Inject

@AndroidEntryPoint
class NetworkChangeReceiver : BroadcastReceiver() {
    
    @Inject
    lateinit var userPreferences: UserPreferences
    
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == ConnectivityManager.CONNECTIVITY_ACTION) {
            val isConnected = isNetworkAvailable(context)
            
            if (isConnected) {
                onNetworkConnected(context)
            } else {
                onNetworkDisconnected(context)
            }
        }
    }
    
    private fun isNetworkAvailable(context: Context): Boolean {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val network = connectivityManager.activeNetwork ?: return false
            val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) ||
                    capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) ||
                    capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)
        } else {
            @Suppress("DEPRECATION")
            val networkInfo = connectivityManager.activeNetworkInfo
            networkInfo?.isConnected == true
        }
    }
    
    private fun onNetworkConnected(context: Context) {
        // Auto-sync when network is available
        if (userPreferences.isAutoSyncEnabled()) {
            val intent = Intent(context, DownloadService::class.java).apply {
                action = DownloadService.ACTION_START_DOWNLOAD
                putExtra(DownloadService.EXTRA_DOWNLOAD_TYPE, DownloadService.DOWNLOAD_TYPE_CACHE_UPDATE)
            }
            context.startForegroundService(intent)
        }
    }
    
    private fun onNetworkDisconnected(context: Context) {
        // Handle network disconnection
        // Could show offline mode notification
    }
}