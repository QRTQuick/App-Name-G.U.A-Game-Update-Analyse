package org.gua.gua.data.local

import android.content.Context
import android.content.SharedPreferences
import dagger.hilt.android.qualifiers.ApplicationContext
import org.gua.gua.data.model.User
import org.gua.gua.data.model.UserStats
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class UserPreferences @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    
    companion object {
        private const val PREFS_NAME = "gua_user_prefs"
        private const val KEY_USERNAME = "username"
        private const val KEY_EMAIL = "email"
        private const val KEY_DISCLAIMER_ACCEPTED = "disclaimer_accepted"
        private const val KEY_IS_LOGGED_IN = "is_logged_in"
        private const val KEY_VIEWED_COUNT = "viewed_count"
        private const val KEY_FAVORITES_COUNT = "favorites_count"
        private const val KEY_REVIEWS_COUNT = "reviews_count"
        private const val KEY_THEME = "theme"
        private const val KEY_AUTO_SYNC = "auto_sync"
        private const val KEY_NOTIFICATIONS_ENABLED = "notifications_enabled"
        private const val KEY_CACHE_SIZE_LIMIT = "cache_size_limit"
        private const val KEY_LANGUAGE = "language"
    }
    
    fun saveUser(user: User) {
        prefs.edit()
            .putString(KEY_USERNAME, user.username)
            .putString(KEY_EMAIL, user.email)
            .putBoolean(KEY_DISCLAIMER_ACCEPTED, user.disclaimerAccepted)
            .putBoolean(KEY_IS_LOGGED_IN, true)
            .apply()
    }
    
    fun getUser(): User? {
        val username = prefs.getString(KEY_USERNAME, null)
        val email = prefs.getString(KEY_EMAIL, null)
        val disclaimerAccepted = prefs.getBoolean(KEY_DISCLAIMER_ACCEPTED, false)
        
        return if (username != null && email != null) {
            User(username, email, disclaimerAccepted)
        } else null
    }
    
    fun getCurrentUser(): User? = getUser()
    
    fun isLoggedIn(): Boolean {
        return prefs.getBoolean(KEY_IS_LOGGED_IN, false)
    }
    
    fun logout() {
        prefs.edit()
            .remove(KEY_USERNAME)
            .remove(KEY_EMAIL)
            .putBoolean(KEY_IS_LOGGED_IN, false)
            .apply()
    }
    
    fun acceptDisclaimer() {
        prefs.edit()
            .putBoolean(KEY_DISCLAIMER_ACCEPTED, true)
            .apply()
    }
    
    fun isDisclaimerAccepted(): Boolean {
        return prefs.getBoolean(KEY_DISCLAIMER_ACCEPTED, false)
    }
    
    fun updateStats(viewed: Int? = null, favorites: Int? = null, reviews: Int? = null) {
        val editor = prefs.edit()
        viewed?.let { editor.putInt(KEY_VIEWED_COUNT, it) }
        favorites?.let { editor.putInt(KEY_FAVORITES_COUNT, it) }
        reviews?.let { editor.putInt(KEY_REVIEWS_COUNT, it) }
        editor.apply()
    }
    
    fun getStats(): UserStats {
        return UserStats(
            viewed = prefs.getInt(KEY_VIEWED_COUNT, 0),
            favorites = prefs.getInt(KEY_FAVORITES_COUNT, 0),
            reviews = prefs.getInt(KEY_REVIEWS_COUNT, 0)
        )
    }
    
    fun incrementViewed() {
        val current = prefs.getInt(KEY_VIEWED_COUNT, 0)
        prefs.edit().putInt(KEY_VIEWED_COUNT, current + 1).apply()
    }
    
    // Theme settings
    fun getTheme(): String {
        return prefs.getString(KEY_THEME, "Dark") ?: "Dark"
    }
    
    fun setTheme(theme: String) {
        prefs.edit().putString(KEY_THEME, theme).apply()
    }
    
    // Auto sync settings
    fun isAutoSyncEnabled(): Boolean {
        return prefs.getBoolean(KEY_AUTO_SYNC, true)
    }
    
    fun setAutoSyncEnabled(enabled: Boolean) {
        prefs.edit().putBoolean(KEY_AUTO_SYNC, enabled).apply()
    }
    
    // Notification settings
    fun areNotificationsEnabled(): Boolean {
        return prefs.getBoolean(KEY_NOTIFICATIONS_ENABLED, true)
    }
    
    fun setNotificationsEnabled(enabled: Boolean) {
        prefs.edit().putBoolean(KEY_NOTIFICATIONS_ENABLED, enabled).apply()
    }
    
    // Cache settings
    fun getCacheSizeLimit(): Long {
        return prefs.getLong(KEY_CACHE_SIZE_LIMIT, 100 * 1024 * 1024) // 100MB default
    }
    
    fun setCacheSizeLimit(sizeInBytes: Long) {
        prefs.edit().putLong(KEY_CACHE_SIZE_LIMIT, sizeInBytes).apply()
    }
    
    // Language settings
    fun getLanguage(): String {
        return prefs.getString(KEY_LANGUAGE, "en") ?: "en"
    }
    
    fun setLanguage(language: String) {
        prefs.edit().putString(KEY_LANGUAGE, language).apply()
    }
}