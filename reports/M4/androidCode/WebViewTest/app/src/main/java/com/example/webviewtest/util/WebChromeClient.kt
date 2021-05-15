package com.example.webviewtest.util

import android.Manifest
import android.content.Context
import android.content.Intent
import android.hardware.Camera
import android.hardware.Camera.CameraInfo
import android.net.Uri
import android.os.Build
import android.os.Environment
import android.os.SystemClock
import android.provider.MediaStore
import android.text.TextUtils
import android.view.View
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.FileProvider
import com.example.webviewtest.BaseApplication
import com.example.webviewtest.MainActivity
import java.io.File
import java.util.*


class WebChromeClient : WebChromeClient() {

    companion object {
        val FILE_PROVIDER_AUTH: String = BaseApplication.instance.packageName.toString() + ".xxx"
        val CAMERA_REQUEST_CODE = 0x2001
        val IMAGE_REQUEST_CODE = 0x2002
    }

    var requestCamaraPath: String? = null

    var filePathCallback: ValueCallback<Array<Uri>>? = null

    private var dirPath: String? = null

    private var menuView: ActionSheet? = null

    override fun onShowFileChooser(webView: WebView?, filePathCallback: ValueCallback<Array<Uri>>?, fileChooserParams: FileChooserParams?): Boolean {

        //Intercept camera calls
        this.filePathCallback = filePathCallback

        var acceptTypes: Array<String?>? = arrayOfNulls(0)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            acceptTypes = fileChooserParams!!.acceptTypes
        }
        dealOpenFileChooser()
        return true
    }


    fun dealOpenFileChooser() {
        val items = arrayOf("Photo", "Camera")
        if (menuView == null) {
            menuView = ActionSheet(MainActivity.mainActivity)
            menuView?.setItemClickListener(object : ActionSheet.ItemClickListener {
                override fun onItemClick(index: Int, btn: View) {
                    val title = (btn as TextView).text.toString()
                    if (index == 0) {
                        try {
                            val intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
                            MainActivity.mainActivity?.startActivityForResult(intent, IMAGE_REQUEST_CODE)
                        } catch (e: Exception) {
                            Toast.makeText(BaseApplication.instance, "No album available", Toast.LENGTH_SHORT).show()
                            filePathCallback(null)
                        }
                    } else if (index == 1) {
                        if (!PermissionUtil.checkPermissionAllGranted(BaseApplication.instance, PermissionUtil.PERMISSION_CAMERA)) {
                            ActivityCompat.requestPermissions(MainActivity.mainActivity!!, arrayOf(Manifest.permission.CAMERA), 0);
                            filePathCallback(null)
                            return
                        }
                        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                        intent.putExtra(MediaStore.Images.Media.ORIENTATION, 0)
                        intent.putExtra(MediaStore.EXTRA_OUTPUT, getPhotoUri())
                        MainActivity.mainActivity?.startActivityForResult(intent, CAMERA_REQUEST_CODE)
                    }
                }
            })
            menuView?.setDismissListener(object : ActionSheet.DismissListener {
                override fun onDismiss(cancel: Boolean) {
                    if (cancel) {
                        filePathCallback(null)
                    }
                }
            })
        }
        menuView?.addItems(items)
        menuView?.show()
    }

    fun getUIri2():Uri?{
        val fileUri = File(Environment.getExternalStorageDirectory().path.toString() + "/" + SystemClock.currentThreadTimeMillis() + ".jpg")
        var imageUri = Uri.fromFile(fileUri)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            imageUri = FileProvider.getUriForFile(BaseApplication.instance, BaseApplication.instance.getPackageName() + ".xxx", fileUri) //通过FileProvider创建一个content类型的Uri
        }
        return imageUri
    }

    /**
     * Call back the selected data to the file control
     */
    fun filePathCallback(results: Array<Uri?>?) {
        if (filePathCallback != null) {
            try {
                filePathCallback?.onReceiveValue(arrayOf(results!!.get(0)!!))
            } catch (e: java.lang.Exception) {
                e.printStackTrace()
                filePathCallback?.onReceiveValue(arrayOf(Uri.EMPTY))
            }
            filePathCallback = null
        }
    }

    private fun checkCameraFacing(facing: Int): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.GINGERBREAD) {
            return false
        }
        val cameraCount = Camera.getNumberOfCameras()
        val info = CameraInfo()
        for (i in 0 until cameraCount) {
            Camera.getCameraInfo(i, info)
            if (facing == info.facing) {
                return true
            }
        }
        return false
    }

    fun getPhotoUri(): Uri? {
        requestCamaraPath = getPhotoTmpPath()
        val context: Context = BaseApplication.instance
        val fileUri: Uri
        fileUri = if (Build.VERSION.SDK_INT >= 24) {
            //Parameter: authority needs to be exactly the same as configured in the manifest file: ${applicationId}.xxx
            FileProvider.getUriForFile(context, context.packageName + ".xxx", File(requestCamaraPath))
        } else {
            Uri.fromFile(File(requestCamaraPath))
        }
        return fileUri
    }

    fun getPhotoTmpPath(): String? {
        val photoName: String = DateUtil.convertDate(Date(), "yyyyMMddHHmss").toString() + "s.jpg"
        val dir: File = File(getDirPath())
        if (!dir.exists()) {
            dir.mkdirs()
        }
        return dirPath + photoName
    }

    fun getDirPath(): String? {
        if (TextUtils.isEmpty(dirPath)) {
            dirPath = FileSavePath.getTempFolder()
        }
        return dirPath
    }

}