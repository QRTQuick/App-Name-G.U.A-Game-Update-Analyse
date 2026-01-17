package org.gua.gua

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class GuaApplication : Application() {
    
    override fun onCreate() {
        super.onCreate()
    }
}