package com.example.stringart.feature.cipher.ui

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.unit.dp

@Composable
fun CipherScreen(state: CipherUiState, onInput: (String) -> Unit, onEncrypt: () -> Unit, onDecrypt: () -> Unit, onClear: () -> Unit, onSettings: () -> Unit) {
    val ctx = LocalContext.current
    val clip = LocalClipboardManager.current
    val saveLauncher = rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("text/plain")) { uri ->
        if (uri != null) saveText(ctx, uri, state.output)
    }
    Column(Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        OutlinedTextField(value = state.input, onValueChange = onInput, label = { Text("Input") }, modifier = Modifier.fillMaxWidth().height(160.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = onEncrypt) { Text("Encrypt") }
            Button(onClick = onDecrypt) { Text("Decrypt") }
            OutlinedButton(onClick = onClear) { Text("Clear") }
            OutlinedButton(onClick = onSettings) { Text("Mapping") }
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedButton(onClick = { clip.getText()?.let { onInput(state.input + it.text) } }) { Text("Paste") }
            OutlinedButton(onClick = { clip.setText(AnnotatedString(state.output)) }) { Text("Copy output") }
            OutlinedButton(onClick = { saveLauncher.launch("cipher_output.txt") }) { Text("Save") }
            OutlinedButton(onClick = { shareText(ctx, state.output) }) { Text("Share") }
        }
        OutlinedTextField(value = state.output, onValueChange = {}, readOnly = true, label = { Text("Output") }, modifier = Modifier.fillMaxWidth().weight(1f))
        state.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    }
}

@Composable
fun MappingEditorScreen(state: CipherUiState, onSave: (String, String) -> Unit, onRemove: (String) -> Unit, onReset: () -> Unit) {
    var k by remember { mutableStateOf("") }
    var v by remember { mutableStateOf("") }
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Row { OutlinedTextField(k, { k = it }, label = { Text("Symbol") }); Spacer(Modifier.width(8.dp)); OutlinedTextField(v, { v = it }, label = { Text("Replacement") }) }
        Row { Button(onClick = { if (k.isNotBlank()) onSave(k, v) }) { Text("Add/Update") }; Spacer(Modifier.width(8.dp)); OutlinedButton(onClick = onReset) { Text("Reset default") } }
        LazyColumn { items(state.mapping.entries.toList()) { (key, value) -> ListItem(headlineContent = { Text("$key → $value") }, trailingContent = { TextButton({ onRemove(key) }) { Text("Remove") } }) } }
    }
}

private fun shareText(ctx: Context, value: String) {
    val intent = Intent(Intent.ACTION_SEND).apply { type = "text/plain"; putExtra(Intent.EXTRA_TEXT, value) }
    ctx.startActivity(Intent.createChooser(intent, "Share cipher output"))
}


private fun saveText(ctx: Context, uri: Uri, value: String) {
    ctx.contentResolver.openOutputStream(uri)?.bufferedWriter()?.use { it.write(value) }
}
