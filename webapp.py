import cv2
import socket
import threading
from flask import Flask, render_template_string, request, jsonify, Response
import mediapipe as mp
import math

app = Flask(__name__)


def vector_2d_angle(v1,v2):
    '''
        求解二维向量的角度
    '''
    v1_x=v1[0]
    v1_y=v1[1]
    v2_x=v2[0]
    v2_y=v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ =65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_
def hand_angle(hand_):
    '''
        获取对应手相关向量的二维角度,根据角度确定手势
    '''
    angle_list = []
    #---------------------------- thumb 大拇指根角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[2][0])- int(hand_[4][0])),(int(hand_[2][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    #---------------------------- index 食指根角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[5][0])),(int(hand_[0][1])- int(hand_[5][1]))),
        ((int(hand_[5][0])- int(hand_[8][0])),(int(hand_[5][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    #---------------------------- middle 中指根角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[9][0])),(int(hand_[0][1])- int(hand_[9][1]))),
        ((int(hand_[9][0])- int(hand_[12][0])),(int(hand_[9][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    #---------------------------- ring 无名指根角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[13][0])),(int(hand_[0][1])- int(hand_[13][1]))),
        ((int(hand_[13][0])- int(hand_[16][0])),(int(hand_[13][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    #---------------------------- pink 小拇指根角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[17][0])),(int(hand_[0][1])- int(hand_[17][1]))),
        ((int(hand_[17][0])- int(hand_[20][0])),(int(hand_[17][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

def h_gesture(angle_list):
    '''
        # 二维约束的方法定义手势
        # fist five gun love one six three thumbup yeah
    '''
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = None
    if 65535. not in angle_list:
        if (angle_list[0]>thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "fist"
        elif (angle_list[0]<thr_angle_s) and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle_s):
            gesture_str = "five"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "gun"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
            gesture_str = "love"
        elif (angle_list[0]>5)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "one"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
            gesture_str = "six"
        elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]>thr_angle):
            gesture_str = "three"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "thumbUp"
        elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "two"
        elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle):
            gesture_str = "four"
        elif (angle_list[0]>thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]<thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "fuck"
        elif (angle_list[0]>thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]<thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "fuck2"
        elif (angle_list[0]>thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle):
            gesture_str = "fuck3"
    return gesture_str

def angle_print(angle_list):
    print('拇指','的根角度是',int(angle_list[0]))
    print('食指','的根角度是',int(angle_list[1]))
    print('中指','的根角度是',int(angle_list[2]))
    print('无名指','的根角度是',int(angle_list[3]))
    print('小指','的根角度是',int(angle_list[4]))



# 初始化摄像头
cap = cv2.VideoCapture(0, device='mipi')  # 0 表示默认摄像头
if not cap.isOpened():
    raise ValueError("无法打开摄像头")
# TCP 服务器相关变量
tcp_server = None
tcp_client = None
server_ip = ""
server_port = 0
rc = "This is the RC data"  # 预定义变量 rc
connected_client_info = None
received_data = ""
send_rc_periodically = False  # 是否周期性发送 rc 数据
rc_send_thread = None

# 定义一个简单的HTML页面
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask TCP Server and Camera</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <h1>Flask TCP Server and Camera</h1>
    <div>
        <label for="ip-port">IP和端口（格式：IP:PORT）：</label>
        <input type="text" id="ip-port" placeholder="192.168.1.1:1234">
        <button id="start-server-btn">启动TCP服务器</button>
        <button id="stop-server-btn">关闭TCP服务器</button>
    </div>
    <div>
        <label for="data-input">输入数据：</label>
        <input type="text" id="data-input" placeholder="输入要发送的数据">
        <button id="send-data-btn">发送数据</button>
        <button id="send-rc-btn">发送RC数据</button>
        <button id="toggle-rc-btn">每秒发送RC数据/停止</button>
    </div>
    <div>
        <h3>已连接的客户端：</h3>
        <div id="connected-client"></div>
        <h3>接收的数据：</h3>
        <div id="received-data"></div>
        <h3>RC数据：</h3>
        <div id="rc-data">{{ rc }}</div>
    </div>
    <h2>摄像头画面</h2>
    <img id="video-feed" src="/video_feed" />

    <script>
        $(document).ready(function() {
            // 启动TCP服务器
            $('#start-server-btn').click(function() {
                var ipPort = $('#ip-port').val();
                $.ajax({
                    url: '/start-server',
                    type: 'POST',
                    data: JSON.stringify({ipPort: ipPort}),
                    contentType: 'application/json',
                    success: function(response) {
                        alert(response.message);
                    },
                    error: function() {
                        alert('启动失败');
                    }
                });
            });

            // 关闭TCP服务器
            $('#stop-server-btn').click(function() {
                $.ajax({
                    url: '/stop-server',
                    type: 'POST',
                    success: function(response) {
                        alert(response.message);
                    },
                    error: function() {
                        alert('关闭失败');
                    }
                });
            });

            // 发送数据
            $('#send-data-btn').click(function() {
                var data = $('#data-input').val();
                $.ajax({
                    url: '/send-data',
                    type: 'POST',
                    data: JSON.stringify({data: data}),
                    contentType: 'application/json',
                    success: function(response) {
                        alert(response.message);
                    },
                    error: function() {
                        alert('发送失败');
                    }
                });
            });

            // 发送RC数据
            $('#send-rc-btn').click(function() {
                $.ajax({
                    url: '/send-rc',
                    type: 'POST',
                    success: function(response) {
                        alert(response.message);
                    },
                    error: function() {
                        alert('发送失败');
                    }
                });
            });

            // 切换每秒发送RC数据
            $('#toggle-rc-btn').click(function() {
                $.ajax({
                    url: '/toggle-rc',
                    type: 'POST',
                    success: function(response) {
                        alert(response.message);
                    },
                    error: function() {
                        alert('操作失败');
                    }
                });
            });

            // 定时更新已连接的客户端和接收的数据
            setInterval(function() {
                $.ajax({
                    url: '/get-status',
                    type: 'GET',
                    success: function(status) {
                        $('#connected-client').text(status.connectedClient || '无客户端连接');
                        $('#received-data').text(status.receivedData || '无数据接收');
                        $('#rc-data').text(status.rcData || '无');
                    }
                });
            }, 1000); // 每2秒更新一次
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """返回HTML页面"""
    return render_template_string(HTML_TEMPLATE, rc=rc)

@app.route('/start-server', methods=['POST'])
def start_server():
    """启动TCP服务器"""
    global tcp_server, server_ip, server_port
    data = request.json
    ip_port = data.get('ipPort', '')
    if not ip_port:
        return jsonify({"message": "IP和端口不能为空！"}), 400

    try:
        server_ip, server_port = ip_port.split(':')
        server_port = int(server_port)
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((server_ip, server_port))
        tcp_server.listen(1)
        threading.Thread(target=accept_client, args=(tcp_server,)).start()
        return jsonify({"message": f"TCP服务器已启动，监听在 {ip_port}"})
    except Exception as e:
        return jsonify({"message": f"启动失败：{str(e)}"}), 500

@app.route('/stop-server', methods=['POST'])
def stop_server():
    """关闭TCP服务器"""
    global tcp_server, tcp_client
    if tcp_server:
        try:
            tcp_server.close()
            tcp_server = None
            if tcp_client:
                tcp_client.close()
                tcp_client = None
            return jsonify({"message": "TCP服务器已关闭"})
        except Exception as e:
            return jsonify({"message": f"关闭失败：{str(e)}"}), 500
    else:
        return jsonify({"message": "TCP服务器未运行"}), 400

def accept_client(server_socket):
    """接受客户端连接"""
    global tcp_client, connected_client_info
    try:
        tcp_client, client_addr = server_socket.accept()
        connected_client_info = f"{client_addr[0]}:{client_addr[1]}"
        print(f"客户端已连接：{client_addr}")
        threading.Thread(target=handle_client, args=(tcp_client,)).start()
    except Exception as e:
        print(f"接受客户端失败：{e}")

def handle_client(client_socket):
    """处理客户端数据"""
    global received_data
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            received_data = data.decode('utf-8')
            print(f"收到数据：{received_data}")
    except Exception as e:
        print(f"处理客户端数据失败：{e}")
    finally:
        client_socket.close()

@app.route('/send-data', methods=['POST'])
def send_data():
    """发送数据到TCP客户端"""
    global tcp_client
    data = request.json
    message = data.get('data', '')
    if not message:
        return jsonify({"message": "数据不能为空！"}), 400

    try:
        if tcp_client:
            tcp_client.sendall(message.encode('utf-8'))
            return jsonify({"message": "数据已发送到客户端"})
        else:
            return jsonify({"message": "没有客户端连接"}), 400
    except Exception as e:
        return jsonify({"message": f"发送失败：{str(e)}"}), 500

@app.route('/send-rc', methods=['POST'])
def send_rc():
    """发送预定义的RC数据到TCP客户端"""
    global tcp_client, rc
    try:
        if tcp_client:
            str_frames='#'+rc+';'
            tcp_client.sendall(str_frames.encode('utf-8'))
            return jsonify({"message": "RC数据已发送到客户端"})
        else:
            return jsonify({"message": "没有客户端连接"}), 400
    except Exception as e:
        return jsonify({"message": f"发送失败：{str(e)}"}), 500

@app.route('/toggle-rc', methods=['POST'])
def toggle_rc():
    """切换每秒发送RC数据的功能"""
    global send_rc_periodically

    if send_rc_periodically:
        send_rc_periodically = False

        return jsonify({"message": "已停止每秒发送RC数据"})
    else:
        send_rc_periodically = True

        return jsonify({"message": "已开始每秒发送RC数据"})



@app.route('/get-status', methods=['GET'])
def get_status():
    global send_rc_periodically, tcp_client, rc,str_frames
    if send_rc_periodically:
        try:
            if tcp_client:
                str_frames='#'+rc+';'
                tcp_client.sendall(str_frames.encode('utf-8'))
                print("RC数据已发送")
            time.sleep(1)
        except Exception as e:
            print(f"周期性发送RC数据失败：{e}")

    """返回已连接的客户端信息和接收的数据"""
    return jsonify({
        "connectedClient": connected_client_info,
        "receivedData": received_data,
        "rcData":rc
    })



def gen_frames():
    global rc
    last_gesture=0
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)
    """生成摄像头画面的帧"""
    while True:
        success, frame = cap.read()
        if not success:
            continue
        else:
            if frame is None:
                continue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame= cv2.flip(frame,1)
            results = hands.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    hand_local = []
                    for i in range(21):
                        x = hand_landmarks.landmark[i].x*frame.shape[1]
                        y = hand_landmarks.landmark[i].y*frame.shape[0]
                        hand_local.append((x,y))
                    if hand_local:
                        angle_list = hand_angle(hand_local)
                        gesture_str = h_gesture(angle_list)
                        cv2.putText(frame,gesture_str,(0,50),0,1.3,(0,0,255),3)
                        rc=gesture_str
            # 将帧转换为JPEG格式

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """返回摄像头画面的响应"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.198.144', port=5000)