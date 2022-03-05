import 'dart:async';
import 'dart:io';

import 'package:csv/csv.dart';
import 'package:flutter/material.dart';
import 'package:orientation/notifiers/api_handler.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:provider/provider.dart';

import 'notifiers/csv_notifier.dart';
import 'notifiers/orientation_notifiers.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, this.title}) : super(key: key);
  final String? title;
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

List<List<String>> _csvData = [];

class _MyHomePageState extends State<MyHomePage> {
  @override
  void initState() {
    var sensorsData = Provider.of<SensorsData>(context, listen: false);

    Timer.periodic(
      const Duration(milliseconds: 200),
      (va) {
        CsvHandler.generateCsvFile(
          accelerometer: sensorsData.accelerometerValues,
          userAcc: sensorsData.userAccelerometerValues,
          gyroscope: sensorsData.gyroscopeValues,
          magnetometer: sensorsData.magnetometerValues,
        );
        if (_csvData.length < 100) {
          _csvData.add([
            ...sensorsData.accelerometerValues,
            ...sensorsData.userAccelerometerValues,
            ...sensorsData.gyroscopeValues,
            ...sensorsData.magnetometerValues,
          ]);
        } else {
          ApiHandler.sendData({"data": _csvData});
          _csvData = [];
        }
      },
    );
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<SensorsData>(
      builder: (context, sensorsData, child) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Sensors Data'),
          ),
          body: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Container(
                padding: const EdgeInsets.all(16.0),
                child: Text('Accelerometer: \n${sensorsData.accelerometerValues}'),
              ),
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text('UserAccelerometer: \n${sensorsData.userAccelerometerValues}'),
              ),
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text('Gyroscope: \n${sensorsData.gyroscopeValues}'),
              ),
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text('Magnetometer: \n${sensorsData.magnetometerValues}'),
              ),
            ],
          ),
        );
      },
    );
  }
}
