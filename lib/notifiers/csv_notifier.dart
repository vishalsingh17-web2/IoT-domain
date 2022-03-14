import 'dart:io';

import 'package:csv/csv.dart';
import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';

class CsvHandler {
  static List<String> headers = [
    "Acceleration_X",
    "Acceleration_Y",
    "Acceleration_Z",
    "User Accelerometer_x",
    "User Accelerometer_y",
    "User Accelerometer_z",
    "Gyroscope_X",
    "Gyroscope_Y",
    "Gyroscope_Z",
    "Magnetometer_X",
    "Magnetometer_Y",
    "Magnetometer_Z"
  ];

  static void generateCsvFile({
    required List<String> accelerometer,
    required List<String> userAcc,
    required List<String> gyroscope,
    required List<String> magnetometer,
    required String name,
  }) async {
    var statuses = await Permission.storage.isGranted;
    print(statuses);
    if (statuses) {
      String file = '/storage/emulated/0/Documents/';
      File f = File(file + name + '.csv');
      print("File created");
      bool checkIfFileExists = await f.exists();
      if (checkIfFileExists) {
        List<List<String>> rows = [
          [...accelerometer, ...userAcc, ...gyroscope, ...magnetometer],
          ["\n"]
        ];
        String csv = const ListToCsvConverter(eol: "\n", fieldDelimiter: ",").convert(rows);
        f.writeAsString(csv, mode: FileMode.append);
        rows = [];
      } else {
        List<List<String>> rows = [
          headers,
          [...accelerometer, ...userAcc, ...gyroscope, ...magnetometer],
          ["\n"]
        ];
        String csv = const ListToCsvConverter(eol: "\n", fieldDelimiter: ",").convert(rows);
        f.writeAsString(csv, mode: FileMode.append);
        rows = [];
      }
    }
  }
}
