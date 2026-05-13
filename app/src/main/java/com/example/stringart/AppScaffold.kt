package com.example.stringart

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.navigation.NavHostController
import com.example.stringart.core.navigation.AppDestinations

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppTopBar(nav: NavHostController) {
    var open by remember { mutableStateOf(false) }
    TopAppBar(title = { Text("3D String Tools") }, actions = {
        IconButton(onClick = { open = true }) { Icon(Icons.Default.MoreVert, null) }
        DropdownMenu(expanded = open, onDismissRequest = { open = false }) {
            listOf(
                "Hole Calculator" to AppDestinations.HoleCalculator,
                "String Art Generator" to AppDestinations.StringArt,
                "G-code Generator" to AppDestinations.GCode,
                "Cipher Encoder" to AppDestinations.Cipher,
                "Settings" to AppDestinations.Settings
            ).forEach { (title, route) ->
                DropdownMenuItem(text = { Text(title) }, onClick = { open = false; nav.navigate(route) })
            }
        }
    })
}
