package com.example.webviewtest.util;

import android.os.Environment;
import android.text.TextUtils;
import com.example.webviewtest.BaseApplication;

import java.io.File;

public class FileSavePath {

    /**
     * 获取应用根文件夹
     *
     * @return
     */
    public static String getStoragePath() {
        String rootpath = "";
        if (Environment.MEDIA_MOUNTED.equals(Environment.getExternalStorageState())
                || !Environment.isExternalStorageRemovable()) {
            rootpath = BaseApplication.instance.getExternalFilesDir(null).getAbsolutePath();
        } else {
            rootpath = BaseApplication.instance.getFilesDir().getAbsolutePath();
        }
        return rootpath + File.separator;
    }

    /**
     * 日志文件夹
     *
     * @return
     */
    public static String getLogFolder() {
        return getStoragePath() + "Log/";
    }

    /**
     * 获取用户的根文件夹
     *
     * @return
     */
    public static String getUserFolder() {
        return getStoragePath() + "/";
    }

    /**
     * 下载的临时文件存放文件夹
     *
     * @return
     */
    public static String getTempFolder() {
        return getUserFolder() + "Temp/";
    }

    /**
     * 附件下载的文件夹
     *
     * @param type 类型
     * @return
     */
    public static String getAttachFolder(String type) {
        return getUserFolder() + "Attach/" + (TextUtils.isEmpty(type) ? "" : type + "/");
    }

    /**
     * 附件下载的文件夹
     *
     * @return
     */
    public static String getAttachFolder() {
        return getAttachFolder("");
    }
}
