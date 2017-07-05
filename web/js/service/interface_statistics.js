function init(){
    data={
        "method":"xx",
        "data":"1234"
    }
    asyncRequest(data, func1,null)
}

function func1(data)
{
    console.log(data)
    var myChart = echarts.init(document.getElementById('main'));
    if (data.code!=1)
    {
        alert(data.msg)
        return 0
    }
    // 指定图表的配置项和数据
    var option = data.result
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
function func2(data)
{
    alert(data)
    console.log(data)
}