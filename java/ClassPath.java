//取得根目录路径
String rootPath = getClass().getResource("/").getFile().toString();

//当前目录路径
String currentPath1 = getClass().getResource(".").getFile().toString();

//当前目录的上级目录路径
String parentPath = getClass().getResource("../").getFile().toString();
