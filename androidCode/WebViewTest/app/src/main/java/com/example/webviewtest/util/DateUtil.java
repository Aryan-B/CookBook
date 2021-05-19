package com.example.webviewtest.util;

import android.text.TextUtils;

import androidx.annotation.Nullable;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class DateUtil {

    /**
     * 12小时制的日期format格式(无毫秒)
     */
    public static String DateFormat_12 = "yyyy-MM-dd hh:mm:ss";

    /**
     * 24小时制的日期format格式(无毫秒)
     */
    public static String DateFormat_24 = "yyyy-MM-dd HH:mm:ss";

    /**
     * 将日期的天转为字符串,不足2为使用0补齐
     *
     * @param day 日期的天数
     * @return 字符串形式的天数
     */
    public static String switchDay(int day) {
        String daystr = day + "";
        if (daystr.length() == 2) {
            return daystr;
        } else {
            return "0" + daystr;
        }
    }

    /**
     * 将日期格式化为指定的形式
     *
     * @param date   日期
     * @param format 日期的格式
     * @return 格式化后的日期字符串
     */
    public static String convertDate(Date date, String format) {
        if (date != null) {
            DateFormat format1 = new SimpleDateFormat(format, Locale.ENGLISH);
            return format1.format(date);
        }
        return "";
    }

    /**
     * 获取当前的年月
     *
     * @return 当前年月的日期字符串 eg:"2019-08"
     */
    public static String getCurrentTimeYM() {
        return convertDate(new Date(), "yyyy-MM");
    }

    /**
     * 获取当前时间的24小时制{@code DateUtil.DateFormat_24}格式
     *
     * @return 当前时间的24小时格式
     */
    public static String getCurrentTime() {
        return convertDate(new Date(), DateFormat_24);
    }

    /**
     * 获取当前时间的小时和分钟格式 HH:mm
     *
     * @return 当前时间的小时和分钟 eg: "15:32"
     */
    public static String getCurrentTimeHM() {
        return convertDate(new Date(), "HH:mm");
    }

    /**
     * 得到指定月的天数
     *
     * @param year  年份
     * @param month 月份
     * @return 指定月份的天数
     */
    public static int getMonthLastDay(int year, int month) {
        Calendar a = Calendar.getInstance();
        a.set(Calendar.YEAR, year);
        a.set(Calendar.MONTH, month - 1);
        a.set(Calendar.DATE, 1);// 把日期设置为当月第一天
        a.roll(Calendar.DATE, -1);// 日期回滚一天，也就是最后一天
        return a.get(Calendar.DATE);
    }

    /**
     * 将数字转为对应的星期数字字符串
     * <p>
     * 1 -> "日"
     * 2 -> "一"
     * 3 -> "二"
     * 4 -> "三"
     * 5 -> "四"
     * 6 -> "五"
     * 7 -> "六"
     * others -> ""
     *
     * @param num 数字
     * @return 星期数字的字符串 eg: "日" "一" "二" "三" "四" "五" "六" ""
     */
    public static String getWeekNameByNum(int num) {
        String name;
        switch (num) {
            case 2:
                name = "一";
                break;
            case 3:
                name = "二";
                break;
            case 4:
                name = "三";
                break;
            case 5:
                name = "四";
                break;
            case 6:
                name = "五";
                break;
            case 7:
                name = "六";
                break;
            case 1:
                name = "日";
                break;
            default:
                name = "";
                break;
        }
        return name;
    }

    /**
     * 根据日期获取星期几字符
     *
     * @param d 日期
     * @return 星期数字的字符串 eg: "日" "一" "二" "三" "四" "五" "六" ""
     */
    public static String getWeekNameByDate(Date d) {
        Calendar ca = Calendar.getInstance();
        ca.setTime(d);
        String name;
        switch (ca.get(Calendar.DAY_OF_WEEK)) {
            case 7:
                name = "六";
                break;
            case 1:
                name = "日";
                break;
            case 2:
                name = "一";
                break;
            case 3:
                name = "二";
                break;
            case 4:
                name = "三";
                break;
            case 5:
                name = "四";
                break;
            case 6:
                name = "五";
                break;
            default:
                name = "";
                break;
        }
        return name;
    }

    /**
     * 将数字转为对应的星期
     * <p>
     * 0 -> "星期日"
     * 1 -> "星期一"
     * 2 -> "星期二"
     * 3 -> "星期三"
     * 4 -> "星期四"
     * 5 -> "星期五"
     * 6 -> "星期六"
     * others -> ""
     *
     * @param day 数字
     * @return 星期数字的字符串 eg: "星期日" "星期一" "星期二" "星期三" "星期四" "星期五" "星期六" ""
     */
    public static String Num2Haizi_Week(int day) {
        switch (day) {
            case 1:
                return "星期一";
            case 2:
                return "星期二";
            case 3:
                return "星期三";
            case 4:
                return "星期四";
            case 5:
                return "星期五";
            case 6:
                return "星期六";
            case 0:
                return "星期日";
            default:
                return "";
        }
    }

    /**
     * 将数字转为对应的星期，其中星期六和星期日带有html的红色字体格式
     * <p>
     * 0 -> "<font color=red>星期日</font>"
     * 1 -> "星期一"
     * 2 -> "星期二"
     * 3 -> "星期三"
     * 4 -> "星期四"
     * 5 -> "星期五"
     * 6 -> "<font color=red>星期六</font>"
     * others -> ""
     *
     * @param day 数字
     * @return 星期数字的字符串 eg: "<font color=red>星期日</font>" "星期一" "星期二" "星期三" "星期四" "星期五" "<font color=red>星期日六/font>" ""
     */
    public static String Num2Haizi_Week_HTML_Color(int day) {
        switch (day) {
            case 1:
                return "星期一";
            case 2:
                return "星期二";
            case 3:
                return "星期三";
            case 4:
                return "星期四";
            case 5:
                return "星期五";
            case 6:
                return "<font color=red>星期六</font>";
            case 0:
                return "<font color=red>星期日</font>";
            default:
                return "";
        }
    }

    /**
     * 将字符串格式的日期转为日期对象
     *
     * @param str       字符串格式的日期
     * @param formatStr 日期的格式
     * @return 日期对象
     */
    @Nullable
    public static Date convertString2Date(String str, String formatStr) {
        DateFormat format = new SimpleDateFormat(formatStr, Locale.CHINA);
        Date date = null;
        try {
            date = format.parse(str);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }

    /**
     * 获取指定的日期，是星期几
     *
     * @param date 日期
     * @return 日期对应的星期：eg："星期一"
     */
    public static String getWeekByDate(Date date) {
        Calendar time = Calendar.getInstance();
        time.clear();
        time.setTime(date);
        int week = time.get(Calendar.DAY_OF_WEEK) - 1;
        return Num2Haizi_Week(week);
    }

    /**
     * 获取指定的日期，是星期几
     *
     * @param date 日期
     * @return 日期对应的星期：eg："一" , "二"
     */
    public static String getWeekByDateSingleChar(Date date) {
        Calendar time = Calendar.getInstance();
        time.clear();
        time.setTime(date);
        int week = time.get(Calendar.DAY_OF_WEEK);
        return getWeekNameByNum(week);
    }

    /**
     * 获取指定的日期是一周的第几天
     * <p>
     * "星期日" -> 0
     * "星期一" -> 1
     * "星期二" -> 2
     * "星期三" -> 3
     * "星期四" -> 4
     * "星期五" -> 5
     * "星期六" -> 6
     *
     * @param date 日期
     * @return 天数
     */
    public static int getWeekByDateTime(Date date) {
        Calendar time = Calendar.getInstance();
        time.setTime(date);
        return time.get(Calendar.DAY_OF_WEEK) - 1;
    }

    /**
     * 根据日期字符串获取星期
     *
     * @param dateStr 日期字符串 格式必须为yyyy-MM-dd
     * @return 星期数字的字符串 eg: "星期日" "星期一" "星期二" "星期三" "星期四" "星期五" "星期六"
     */
    public static String getWeekByDateStr(String dateStr) {
        Calendar time = Calendar.getInstance();
        time.clear();
        time.setTime(convertString2Date(dateStr, "yyyy-MM-dd"));
        int week = time.get(Calendar.DAY_OF_WEEK) - 1;
        return Num2Haizi_Week(week);
    }

    /**
     * 根据日期字符串获取 带有html颜色格式的星期
     *
     * @param date 日期
     * @return 带有html颜色格式的星期 {@link #Num2Haizi_Week_HTML_Color(int)}
     */
    public static String getWeekByDate_HTML_Color(Date date) {
        Calendar time = Calendar.getInstance();
        time.clear();
        time.setTime(date);
        int week = time.get(Calendar.DAY_OF_WEEK) - 1;
        return Num2Haizi_Week_HTML_Color(week);
    }

    /**
     * yyyy-MM-dd 格式的日期获取对应的星期
     *
     * @param s yyyy-MM-dd 格式的日期字符串
     * @return 日期对应的星期：eg："星期一"
     */
    public static String getWeekByFormatedDateStr(String s) {
        Calendar time = Calendar.getInstance();
        String[] ss = s.split("-");
        time.set(Integer.parseInt(ss[0]), Integer.parseInt(ss[1]) - 1, Integer.parseInt(ss[2]));
        return getWeekByDate(time.getTime());
    }

    /**
     * yyyy-MM-dd 格式的日期获取对应的 带有html颜色格式的星期
     *
     * @param s yyyy-MM-dd 格式的日期字符串
     * @return 带有html颜色格式的星期 {@link #Num2Haizi_Week_HTML_Color(int)}
     */
    public static String getWeekByFormatedDateStr_HTML_Color(String s) {
        Calendar time = Calendar.getInstance();
        String[] ss = s.split("-");
        time.set(Integer.parseInt(ss[0]), Integer.parseInt(ss[1]) - 1, Integer.parseInt(ss[2]));
        return getWeekByDate_HTML_Color(time.getTime());
    }

    /**
     * 获取当前日期是这个月的第几天
     *
     * @return
     */
    public static int getDayNumsOfCurrentMonth() {
        Calendar time = Calendar.getInstance();
        return time.getActualMaximum(Calendar.DAY_OF_MONTH);
    }

    /**
     * 获取当前日期是星期几
     *
     * @return 星期数字的字符串 eg: "星期日" "星期一" "星期二" "星期三" "星期四" "星期五" "星期六"
     */
    public static String getWeektimeOfCurrentTime() {
        Calendar time = Calendar.getInstance();
        int week = time.get(Calendar.DAY_OF_WEEK) - 1;
        return Num2Haizi_Week(week);
    }

    /**
     * 获取指定日期的月份的总天数
     *
     * @param date 日期
     * @return 日期的月份总天数
     */
    public static int getDayNumsOfMonth(Date date) {
        Calendar time = Calendar.getInstance();
        time.setTime(date);
        return time.getActualMaximum(Calendar.DAY_OF_MONTH);
    }

    /**
     * 获取指定年月的月份总天数
     *
     * @param year  年份
     * @param month 实际月份 1-12
     * @return 月份的总天数
     */
    public static int getDaysOfYM(int year, int month) {
        Calendar time = Calendar.getInstance();
        time.clear();
        time.set(Calendar.YEAR, year);
        time.set(Calendar.MONTH, month - 1);
        return time.getActualMaximum(Calendar.DAY_OF_MONTH);
    }

    /**
     * 将指定的数字转为字符串，不足2位数补0
     *
     * @param i 数字
     * @return 对应的字符串，不足2位数补0
     */
    public static String AddZero(int i) {
        if (i >= 0 && i <= 9) {
            return "0" + i;
        }
        return String.valueOf(i);

    }

    /**
     * 将日期格式以 tag  分割，转为yyyy-MM-dd 格式
     *
     * @param strs 日期字符串
     * @param tag  分隔符
     * @return yyyy-MM-dd 格式的日期
     */
    public static String getFormatedDate(String strs, String tag) {
        String[] ss = strs.split(tag);
        String year = ss[0];
        String month = switchDay(Integer.parseInt(ss[1]));
        String day = switchDay(Integer.parseInt(ss[2]));
        return year + "-" + month + "-" + day;
    }

    /**
     * 获取当前年月日,时分秒字符串
     *
     * @return 当前日期字符串 格式：yyyy/MM/dd HH:mm:ss
     */
    public static String getTimeStrHanzi() {
        return convertDate(new Date(), "yyyy/MM/dd HH:mm:ss");
    }

    /**
     *  获取当前年份总周数
     *
     * @return 当前年份总周数
     */
    public static int getWeeksOfYear() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        Calendar cl = Calendar.getInstance();
        int year = cl.get(Calendar.YEAR);
        try {
            cl.setTime(sdf.parse(year + "-12-31"));
            int i = cl.get(Calendar.DAY_OF_WEEK);
            cl.setTime(sdf.parse(year + "-12-" + (31 - i)));
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return cl.get(Calendar.WEEK_OF_YEAR);
    }

    /**
     *  获取指定年份总周数
     *
     * @param year 年份
     * @return 指定年份总周数
     */
    public static int getWeeksOfYear(int year) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        Calendar cl = Calendar.getInstance();
        try {
            cl.setTime(sdf.parse(year + "-12-31"));
            int i = cl.get(Calendar.DAY_OF_WEEK);
            cl.setTime(sdf.parse(year + "-12-" + (31 - i)));
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return cl.get(Calendar.WEEK_OF_YEAR);
    }

    /**
     * 获取当前时间的 MM-dd HH:mm 的格式字符串
     *
     * @return 当前时间的 MM-dd HH:mm 的格式字符串
     */
    public static String getListUpdateStr() {
        return new SimpleDateFormat("MM-dd HH:mm").format(new Date(System.currentTimeMillis()));
    }

    /**
     * 计算当前日期与参数日期的差值 参数日期 小于 当前日期
     *
     * @param dateStr
     * @return
     */
    public static int getDateStrFromOneDayToToday(String dateStr) {
        SimpleDateFormat sdf;
        if (dateStr.contains("/")) {
            sdf = new SimpleDateFormat("yyyy/MM/dd");
        } else {
            sdf = new SimpleDateFormat("yyyy-MM-dd");
        }
        Date oneday;
        try {
            oneday = sdf.parse(dateStr);
            Calendar cal = Calendar.getInstance();
            cal.setTime(oneday);
            long time1 = cal.getTimeInMillis();
            cal.setTime(convertString2Date(getCurrentTime(), "yyyy-MM-dd"));
            long time2 = cal.getTimeInMillis();
            long between_days = (time2 - time1) / (1000 * 3600 * 24);
            return Integer.parseInt(String.valueOf(between_days));
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return 0;
    }

    /**
     * 与现在的时间比较,更改2天之内的时间格式
     *
     * @param datetime 格式：yyyy-MM-dd HH:mm:ss
     * @return 前天/昨天/今天
     */
    public static String getDateStr(String datetime) {
        if (TextUtils.isEmpty(datetime)) {
            return "";
        }
        String[] datetimes = datetime.split(" ");
        String date = datetimes[0];
        String time = datetimes.length > 1 ? datetimes[1] : "";
        if (time.length() > 5) {
            time = time.substring(0, time.lastIndexOf(":"));
        }
        String nowdate = getCurrentTime().split(" ")[0];
        String beforeDay = getSpecifiedDayBefore(nowdate);
        String bbeforeDay = getSpecifiedDayBefore(beforeDay);
        if (date.equals(nowdate)) {
            return time;
        }
        if (beforeDay.equals(date)) {
            return "昨天";
        }
        if (bbeforeDay.equals(date)) {
            return "前天";
        }
        return date;
    }

    /**
     * 获得指定日期的前一天
     *
     * @param specifiedDay yyyy-MM-dd 格式的日期
     * @return 前一天的日期
     */
    public static String getSpecifiedDayBefore(String specifiedDay) {
        Calendar c = Calendar.getInstance();
        SimpleDateFormat sd = new SimpleDateFormat("yyyy-MM-dd");
        Date date = null;
        try {
            date = sd.parse(specifiedDay);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        c.setTime(date);
        int day = c.get(Calendar.DATE);
        c.set(Calendar.DATE, day - 1);

        return sd.format(c.getTime());
    }

    /**
     * 比较2个时间大小 2个时间参数格式必须一致
     *
     * @param time1 第一个时间
     * @param time2 第二个时间
     * @return >0 time1晚 ; <0 time2晚 ; =0 时间一样
     */
    public static long timeLag(String time1, String time2) {
        return time1.compareTo(time2);
    }

    /**
     * 根据详细日期 获得时间
     *
     * @param datetime yyyy/MM/dd HH:mm:ss 格式的日期
     * @return 给定日期的 HH:mm 格式的时间
     */
    public static String getTimeByDateTimeStr(String datetime) {
        String timeStr = "";
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
        SimpleDateFormat sdftime = new SimpleDateFormat("HH:mm");
        try {
            Date timedate = sdf.parse(datetime);
            timeStr = sdftime.format(timedate);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return timeStr;
    }

    /**
     * 根据详细日期 获得日期
     *
     * @param datetime yyyy/MM/dd HH:mm:ss 格式的日期
     * @return 给定日期的 yyyy/MM/dd 格式
     */
    public static String getDateByDateTime(String datetime) {
        String timeStr = "";
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
        SimpleDateFormat sdftime = new SimpleDateFormat("yyyy/MM/dd");
        try {
            Date timedate = sdf.parse(datetime);
            timeStr = sdftime.format(timedate);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return timeStr;
    }
}
