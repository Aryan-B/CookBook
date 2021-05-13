package com.example.webviewtest.util;

import android.app.Activity;
import android.content.Context;
import android.graphics.PixelFormat;
import android.os.Build;
import android.os.IBinder;
import android.text.TextUtils;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnKeyListener;
import android.view.ViewGroup;
import android.view.ViewTreeObserver;
import android.view.WindowManager;
import android.widget.LinearLayout;
import android.widget.PopupWindow;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.core.content.ContextCompat;

import com.example.webviewtest.R;

import java.util.Arrays;
import java.util.List;

public class ActionSheet extends PopupWindow implements View.OnClickListener {

    protected Activity context;

    private WindowManager wm;

    private View maskView;

    private ItemClickListener itemClickListener;

    private DismissListener dismissListener;

    private LinearLayout parentView;

    private TextView cancelTv;

    private ScrollView sv;

    /**
     * 提示信息
     */
    private String prompt;

    /**
     * 选项高度
     */
    private int itemHeight;

    private boolean isCancel = true;

    public ActionSheet(Activity context) {
        super(context);
        this.context = context;
        wm = (WindowManager) context.getSystemService(Context.WINDOW_SERVICE);
        itemHeight = DensityUtil.dip2px(context, 45);
        initType();
        initView();
    }

    public View initView() {
        View view = LayoutInflater.from(context).inflate(R.layout.frm_popup_actionsheet_menu, null);
        parentView = (LinearLayout) view.findViewById(R.id.ll_item);
        sv = (ScrollView) view.findViewById(R.id.sv);
        cancelTv = (TextView) view.findViewById(R.id.tv_cancel_item);
        cancelTv.setOnClickListener(this);
        setContentView(view);
        setWidth(ViewGroup.LayoutParams.MATCH_PARENT);
        setHeight(ViewGroup.LayoutParams.WRAP_CONTENT);
        setOutsideTouchable(true);
        setBackgroundDrawable(ContextCompat.getDrawable(context, android.R.color.transparent));
        setAnimationStyle(R.style.Animations_BottomPush);
        return view;
    }

    public void setPrompt(String prompt) {
        this.prompt = prompt;
    }

    private void initType() {
        // 解决华为手机在home建进入后台后，在进入应用，蒙层出现在popupWindow上层的bug。
        // android4.0及以上版本都有这个hide方法，根据jvm原理，可以直接调用，选择android6.0版本进行编译即可。
        if (Build.VERSION.SDK_INT > 22) {
            setWindowLayoutType(WindowManager.LayoutParams.TYPE_APPLICATION_SUB_PANEL);
        }
        //因为某些机型是虚拟按键的,所以要加上以下设置防止挡住按键.
        setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);
    }

    @Override
    public void showAtLocation(View parent, int gravity, int x, int y) {
        addMaskView(parent.getWindowToken());
        super.showAtLocation(parent, gravity, x, y);
        isCancel = true;
    }

    @Override
    public void showAsDropDown(View anchor, int xoff, int yoff) {
        addMaskView(anchor.getWindowToken());
        super.showAsDropDown(anchor, xoff, yoff);
    }

    @Override
    public void dismiss() {
        removeMaskView();
        super.dismiss();
        if (dismissListener != null) {
            dismissListener.onDismiss(isCancel);
        }
    }

    public void addItems(String title) {
        addItems(new String[]{title});
    }

    public void addItems(String title1, String title2) {
        addItems(new String[]{title1, title2});
    }

    public void addItems(String title1, String title2, String title3) {
        addItems(new String[]{title1, title2, title3});
    }

    public void addItems(String[] titles) {
        setScrollViewHeight(sv);
        parentView.removeAllViews();
        if (titles == null || titles.length == 0) {
            return;
        }
        List<String> items = Arrays.asList(titles);
        if (!TextUtils.isEmpty(prompt)) {
            addPrompt();
        }
        for (int i = 0; i < items.size(); i++) {
            if (i > 0) {
                LinearLayout ll = new LinearLayout(context);
                ll.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 1));
                ll.setBackgroundResource(R.color.line);
                parentView.addView(ll);
            }

            int backgroud;
            backgroud = R.drawable.frm_click_item_bg;
            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, itemHeight);
            TextView tv = new TextView(context);
            tv.setGravity(Gravity.CENTER);
            tv.setLayoutParams(lp);
            tv.setBackgroundResource(backgroud);
            tv.setTextSize(16);
            tv.setText(items.get(i));
            tv.setTextColor(ContextCompat.getColor(context, R.color.black));
            tv.setTag(i);
            tv.setOnClickListener(this);
            parentView.addView(tv);
        }
    }

    private void addPrompt() {
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, itemHeight);
        TextView tv = new TextView(context);
        tv.setGravity(Gravity.CENTER);
        tv.setLayoutParams(lp);
        tv.setBackgroundResource(R.drawable.frm_click_cardtop_bg);
        tv.setTextSize(14);
        tv.setText(prompt);
        tv.setTextColor(ContextCompat.getColor(context, R.color.text_grey));
        parentView.addView(tv);
        LinearLayout ll = new LinearLayout(context);
        ll.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 1));
        ll.setBackgroundResource(R.color.line);
        parentView.addView(ll);
    }

    /**
     * 显示在界面的底部
     */
    public void show() {
        if (parentView.getChildCount() > 0 && !isShowing()) {
            showAtLocation(context.getWindow().getDecorView(), Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL, 0, 0);
        }
    }

    /**
     * 取消按钮的标题文字
     *
     * @param title
     * @return
     */
    public void setCancelButtonText(String title) {
        cancelTv.setText(title);
    }

    /**
     * 取消按钮的标题文字
     *
     * @param strId
     * @return
     */
    public void setCancelButtonText(int strId) {
        setCancelButtonText(context.getString(strId));
    }

    public void setDismissListener(DismissListener dismissListener) {
        this.dismissListener = dismissListener;
    }

    public void setItemClickListener(ItemClickListener itemClickListener) {
        this.itemClickListener = itemClickListener;
    }

    @Override
    public void onClick(View v) {
        int index = -1;
        if (v.getTag() != null) {
            index = (Integer) v.getTag();
            //点击了选项，标记当前不是取消操作
            isCancel = false;
        } else {
            //未点击选项，标记当前为取消操作
            isCancel = true;
        }
        dismiss();
        if (itemClickListener != null) {
            if (v.getTag() != null) {
                itemClickListener.onItemClick(index, v);
            }
        }
    }

    public interface DismissListener {
        /**
         * @param cancel 是否取消选择，true表示点击了取消按钮或者返回按钮或者点击空白；false表示点击了选项
         */
        void onDismiss(boolean cancel);
    }

    public interface ItemClickListener {
        void onItemClick(int index, View btn);
    }

    private void addMaskView(IBinder token) {
        WindowManager.LayoutParams p = new WindowManager.LayoutParams();
        p.width = WindowManager.LayoutParams.MATCH_PARENT;
        p.height = WindowManager.LayoutParams.MATCH_PARENT;
        p.format = PixelFormat.TRANSLUCENT;
        p.type = WindowManager.LayoutParams.TYPE_APPLICATION_PANEL;
        p.token = token;
        p.windowAnimations = android.R.style.Animation_Toast;
        maskView = new View(context);
        maskView.setBackgroundColor(0x7f000000);
        maskView.setFitsSystemWindows(false);
        // 华为手机在home建进入后台后，在进入应用，蒙层出现在popupWindow上层，导致界面卡死，
        // 这里新增加按bug返回。
        // initType方法已经解决该问题，但是还是留着这个按back返回功能，防止其他手机出现华为手机类似问题。
        maskView.setOnKeyListener(new OnKeyListener() {
            @Override
            public boolean onKey(View v, int keyCode, KeyEvent event) {
                if (keyCode == KeyEvent.KEYCODE_BACK) {
                    //点击返回按钮，标记为取消操作
                    isCancel = true;
                    dismiss();
                    return true;
                }
                return false;
            }
        });
        wm.addView(maskView, p);
    }

    private void removeMaskView() {
        if (maskView != null && wm != null) {
            wm.removeViewImmediate(maskView);
            maskView = null;
        }
    }

    /**
     * 1.设置ScrollView的高度
     * 2.设置一定条数，不能再撑开，而是变成滑动
     *
     * @param sv
     */
    private void setScrollViewHeight(final ScrollView sv) {
        sv.getViewTreeObserver().addOnGlobalLayoutListener(new ViewTreeObserver.OnGlobalLayoutListener() {
            @Override
            public void onGlobalLayout() {
                /**
                 * 最小可滑动条数
                 */
                int minNumWhenScroll = 10;
                /**
                 * LinearLayout中子布局的数量
                 */
                int childViewCount = parentView.getChildCount();
                /**
                 * ScrollView的高度
                 */
                int scrollLayoutHeight = 0;
                /**
                 * LinearLayout中一个TextView的高度
                 */
                int childHeight = 0;
                /**
                 * LinearLayout中TextView的数量
                 */
                int count = 0;
                for (int i = 0; i < childViewCount; i++) {
                    if (parentView.getChildAt(i) instanceof TextView) {
                        count++;
                    }
                }
                if (count == 0) {
                    scrollLayoutHeight = 0;
                } else {
                    childHeight = parentView.getChildAt(0).getHeight();
                    if (count <= minNumWhenScroll) {
                        scrollLayoutHeight = childHeight * count;
                        scrollLayoutHeight += count;
                    } else {
                        scrollLayoutHeight = childHeight * minNumWhenScroll;
                    }
                }
                sv.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, scrollLayoutHeight));
                sv.getViewTreeObserver().removeGlobalOnLayoutListener(this);
            }
        });
    }
}