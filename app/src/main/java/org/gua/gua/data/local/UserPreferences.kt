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
}