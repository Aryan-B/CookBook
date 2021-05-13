package com.example.webviewtest

import android.annotation.SuppressLint
import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.View
import android.view.WindowManager
import android.webkit.*
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.example.webviewtest.util.WebChromeClient
import com.example.webviewtest.util.WebChromeClient.Companion.CAMERA_REQUEST_CODE
import com.example.webviewtest.util.WebChromeClient.Companion.IMAGE_REQUEST_CODE


class MainActivity : AppCompatActivity() {

    companion object {
        var mainActivity: MainActivity? = null
    }

    var webChromeClient: WebChromeClient? = null

    @SuppressLint("SetJavaScriptEnabled")
    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mainActivity = this
        setContentView(R.layout.activity_main)
        val webView = findViewById<WebView>(R.id.wb_test)


        if(supportActionBar !=null){
            supportActionBar?.hide()

        }
        window.statusBarColor = resources.getColor(R.color.black)

        //Set the URL that needs to be loaded
        webView.loadUrl("http://18.221.82.143:3000")

        webChromeClient = WebChromeClient()
        webView.webChromeClient = webChromeClient


        val settings = webView.settings
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            settings.mixedContentMode = WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
        }
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true

        //The system will open the web page through the mobile browser by default, in order to be able to display the web page directly through WebView, you must set
        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                super.onPageStarted(view, url, favicon)
            }

            override fun shouldOverrideUrlLoading(view: WebView, url: String): Boolean {
                view.loadUrl(url)
                return true
            }

            override fun shouldInterceptRequest(view: WebView?, request: WebResourceRequest?): WebResourceResponse? {
                return super.shouldInterceptRequest(webView, request)
            }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (resultCode == RESULT_OK) {
            if (requestCode == CAMERA_REQUEST_CODE) {
                //System photo result processing
                webChromeClient?.filePathCallback(arrayOf(webChromeClient?.getPhotoUri()))
            } else if (requestCode == IMAGE_REQUEST_CODE) {
                //Select album result processing
                var results: Array<Uri?>? = null
                val dataString = data?.dataString
                val clipData = data?.clipData
                if (clipData != null) {
                    results = arrayOfNulls(clipData.itemCount)
                    for (i in 0 until clipData.itemCount) {
                        val item = clipData.getItemAt(i)
                        results[i] = item.uri
                    }
                }
                if (dataString != null) {
                    results = arrayOf(Uri.parse(dataString))
                }
                webChromeClient?.filePathCallback(results)
            }
        } else {
            webChromeClient?.filePathCallback(null)
        }
        super.onActivityResult(requestCode, resultCode, data)
    }

}