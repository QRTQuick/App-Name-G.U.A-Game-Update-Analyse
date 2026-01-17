package org.gua.gua.ui

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.setupWithNavController
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.R
import org.gua.gua.databinding.ActivityMainBinding

@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        try {
            binding = ActivityMainBinding.inflate(layoutInflater)
            setContentView(binding.root)
            
            setupNavigation()
        } catch (e: Exception) {
            e.printStackTrace()
            // Fallback to basic layout if binding fails
            setContentView(R.layout.activity_main)
        }
    }
    
    private fun setupNavigation() {
        try {
            val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as? NavHostFragment
            navHostFragment?.let { fragment ->
                val navController = fragment.navController
                binding.bottomNavigation.setupWithNavController(navController)
            }
        } catch (e: Exception) {
            e.printStackTrace()
            // Hide bottom navigation if setup fails
            binding.bottomNavigation.visibility = android.view.View.GONE
        }
    }
}