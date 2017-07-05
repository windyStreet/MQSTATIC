function getDBCODE()
{
    var DBCODE = {};
    DBCODE.EQ = 11;  // 相等
    DBCODE.NE = 21; // 不相等
    DBCODE.LT = 12;  // 小于
    DBCODE.GT = 13;  // 大于
    DBCODE.LTE = 121;  // 小于等于
    DBCODE.GTE = 131;  // 大于等于
    DBCODE.IN = 14;  // in
    DBCODE.NIN = 24;  // not in
    DBCODE.OR = 15; // 或者
    DBCODE.AND = 16; // 并且
    DBCODE.NOT = 17; // 取反
    return DBCODE;
}