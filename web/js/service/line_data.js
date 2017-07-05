function init(){
    DBCODE = getDBCODE()
    //选取的不能大于当前值。备注：如果数据未计算，应该先采用数据恢复方案，恢复数据之后再操作
//    bbt_login_sUserLogin
//    FR_trDs_uStudyRecord
//    bbt_course_uStudyRecordByAndroid
//    bbt_course_uStudyRecord_offlineByAndroid
//    bbt_course_uStudyRecordByIos
//    bbt_course_uStudyRecord_offlineByIos
    data={
        "method":"line_test",
        "data":{
            "type":"line",
            "step_count":300,
            "step":1,
            "legend_infos":{
                "接口调用总量":
                {
                    "project_name":"YXYBB",
                    "statistic_type":"interface",
                    "statistic_name":"",
                    "filter_infos":[]
                    //"filter_infos":[{"key":"time","value":"2017-05-19 10:00:00.12","relation":DBCODE.GT},{"key":"time","value":"2017-05-22 11:10:12.12","relation":DBCODE.LTE},{"key":"name","value":"bbt_login_sUserLogin","relation":DBCODE.EQ}],
                },
                "用户登录接口":
                {
                    "project_name":"YXYBB",
                    "statistic_type":"interface",
                    "statistic_name":"bbt_login_sUserLogin",
                    "filter_infos":[]
                    //"filter_infos":[{"key":"time","value":"2017-05-19 10:00:00.12","relation":DBCODE.GT},{"key":"time","value":"2017-05-22 11:10:12.12","relation":DBCODE.LTE},{"key":"name","value":"FR_trDs_uStudyRecord","relation":DBCODE.EQ}],
                },
                "学习记录更新接口":
                {
                    "project_name":"YXYBB",
                    "statistic_type":"interface",
                    "statistic_name":"FR_trDs_uStudyRecord",
                    "filter_infos":[]
                },
                "安卓线上学习记录更新接口":
                {
                    "project_name":"YXYBB",
                    "statistic_type":"interface",
                    "statistic_name":"bbt_course_uStudyRecordByAndroid",
                    "filter_infos":[]
                },
                "安卓离线学习记录更新接口":
                {
                    "project_name":"YXYBB",
                    "statistic_type":"interface",
                    "statistic_name":"bbt_course_uStudyRecord_offlineByAndroid",
                    "filter_infos":[]
                },
                "ios线上学习记录更新接口":
                {
                    "project_name":"YXYBB",
                    "statistic_type":"interface",
                    "statistic_name":"bbt_course_uStudyRecordByIos",
                    "filter_infos":[]
                },
                "ios离线学习记录更新接口":
                {
                    "project_name":"YXYBB",
                    "statistic_type":"interface",
                    "statistic_name":"bbt_course_uStudyRecord_offlineByIos",
                    "filter_infos":[]
                }
            },
            "title_text":"接口调用量统计"
           }
    }
    asyncRequest(data, func1,null)
}

function func1(data)
{

    var myChart = echarts.init(document.getElementById('main'));
    if (data.code!=1)
    {
        alert(data.msg)
        return 0
    }
    // 指定图表的配置项和数据
    var option = data.result
    console.log(option)
    option['series']['showSymbol']=false
    option['series']['smooth']= true
    option['tooltip']= { trigger: 'axis'}
    option['grid']=  {left: '3%', right: '4%',bottom: '3%',containLabel: true}
    option['toolbox'] = {feature: {saveAsImage: {}}}
    option['xAxis']['type']='category'
    option['xAxis']['boundaryGap']=false
    option['yAxis']={type: 'value'}
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}