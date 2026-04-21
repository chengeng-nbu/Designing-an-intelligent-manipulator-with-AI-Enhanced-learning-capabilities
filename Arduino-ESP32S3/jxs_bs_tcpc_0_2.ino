#include <WiFi.h>
#include <string.h>

const char *ssid = "iQOO Neo9";
const char *password = "00000000";

const IPAddress serverIP(192,168,198,144); //欲访问的地址
uint16_t serverPort = 6012;         //服务器端口号

WiFiClient client; //声明一个客户端对象，用于与服务器进行连接

int PINx[5]={38,39,40,41,42};
int i=0;

String CMD_Data_Buff="";

void Serial1_RxTx_String(int Rx,int Tx,String Data){//初始化串口数据发送
  Serial1.begin(115200,SERIAL_8N1,Rx,Tx);
  Serial1.print(Data);
  delay(10);
}

void Motor_Step_(int Not_default){//初始化手指数据转发
  if(Not_default!=PINx[0])Serial1_RxTx_String(0,PINx[0],"#id:b40;#id:c75;");
  if(Not_default!=PINx[1])Serial1_RxTx_String(0,PINx[1],"#id:d75;#id:e75;#id:f75;");
  if(Not_default!=PINx[2])Serial1_RxTx_String(0,PINx[2],"#id:g75;#id:h75;#id:i75;");
  if(Not_default!=PINx[3])Serial1_RxTx_String(0,PINx[3],"#id:j75;#id:k75;#id:l75;");
  if(Not_default!=PINx[4])Serial1_RxTx_String(0,PINx[4],"#id:m75;#id:n75;#id:o75;");
}

void CMD_Data(String CMD_Data_Buff){
  String data_CMD="";
  int temp=0;
  if(CMD_Data_Buff[0]=='#'){
    if(CMD_Data_Buff[3]!=':'){
      while(CMD_Data_Buff[temp]!=';'){
        data_CMD+=CMD_Data_Buff[temp++];
      }
      if(data_CMD=="#five"){
        Serial1_RxTx_String(0,PINx[0],"#id:b00;#id:c00;");
        Serial1_RxTx_String(0,PINx[1],"#id:d00;#id:e00;#id:f00;");
        Serial1_RxTx_String(0,PINx[2],"#id:g00;#id:h00;#id:i00;");
        Serial1_RxTx_String(0,PINx[3],"#id:j00;#id:k00;#id:l00;");
        Serial1_RxTx_String(0,PINx[4],"#id:m00;#id:n00;#id:o00;");
      }
      if (data_CMD=="#fist"){
          Motor_Step_(0);
      }
      if(data_CMD=="#thumbUp"){
          Motor_Step_(PINx[0]);
          Serial1_RxTx_String(0,PINx[0],"#id:b00;#id:c00;");
      }
      if(data_CMD=="#one"){
          Motor_Step_(PINx[1]);
          Serial1_RxTx_String(0,PINx[1],"#id:d00;#id:e00;#id:f00;");
      }
      if(data_CMD=="#fuck"){
          Motor_Step_(PINx[2]);
          Serial1_RxTx_String(0,PINx[2],"#id:g00;#id:h00;#id:i00;");
      }
      if(data_CMD=="#fuck2"){
          Motor_Step_(PINx[3]);
          Serial1_RxTx_String(0,PINx[3],"#id:j00;#id:k00;#id:l00;");
      }
      if(data_CMD=="#fuck3"){
          Motor_Step_(PINx[4]);
          Serial1_RxTx_String(0,PINx[4],"#id:m00;#id:n00;#id:o00;");
      }
    }else{
      Serial1_RxTx_String(0,PINx[(CMD_Data_Buff[4]-'a')/3],CMD_Data_Buff);

    }
  }
}

void setup()
{
    Serial.begin(115200);
    Serial.println();
    Serial.onReceive(Collect_Callback);  //开启串口中断接收调试数据
    pinMode(2, INPUT);
    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false); //关闭STA模式下wifi休眠，提高响应速度
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected");
    Serial.print("IP Address:");
    Serial.println(WiFi.localIP());
    Serial1.begin(115200, SERIAL_8N1, 0, PINx[0]);
    
}

void loop()
{
    Serial.println("尝试访问服务器");
    if (client.connect(serverIP, serverPort)) //尝试访问目标地址
    {
        Serial.println("访问成功");

        client.print("Hello world!");                    //向服务器发送数据
        while (client.connected() || client.available()) //如果已连接或有收到的未读取的数据
        {
            if (client.available()) //如果有数据可读取
            {
                String line = client.readString(); //读取数据到换行符
                CMD_Data(line);
                Serial.print("读取到数据：");
                Serial.println(line);
                client.write(line.c_str()); //将收到的数据回发
            }
        }
        Serial.println("关闭当前连接");
        client.stop(); //关闭客户端
    }
    else
    {
        Serial.println("访问失败");
        client.stop(); //关闭客户端

    }
    delay(5000);
}

void Collect_Callback(){               
  String Collect_Data = "";                     //定义一个String类型的变量
  while(Serial.available()){                 //用While判断缓冲区是否有内容
    Collect_Data += char(Serial.read());     //取出缓冲区内容
  } 
  CMD_Data_Buff=Collect_Data;
  Serial.print(Collect_Data);                     //输出取出的内容
  CMD_Data(CMD_Data_Buff);
  Collect_Data = "";                              //清空内容
 }

