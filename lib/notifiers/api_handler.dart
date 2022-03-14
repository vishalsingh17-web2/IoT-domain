import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiHandler {
  static String baseUrl = 'http://172.16.31.95:3000/api';
  static String sendSensorData = baseUrl + '/send';

  static Future<dynamic> sendData(Map<String, dynamic> data) async {
    var response = await http.post(Uri.parse(sendSensorData), body: jsonEncode(data));
    print(response.body);
    return response.body;
  }
}
