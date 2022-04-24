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
  const MyHomePage({Key? key, required this.url}) : super(key: key);
  final String url;
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

List<double> _csvData = [];
List<double> accel = [];

class _MyHomePageState extends State<MyHomePage> {
  String status = "";
  @override
  void initState() {
    var sensorsData = Provider.of<SensorsData>(context, listen: false);

    Timer.periodic(
      const Duration(milliseconds: 200),
      (va) async {
        // CsvHandler.generateCsvFile(
        //   accelerometer: sensorsData.accelerometerValues,
        //   userAcc: sensorsData.userAccelerometerValues,
        //   gyroscope: sensorsData.gyroscopeValues,
        //   magnetometer: sensorsData.magnetometerValues,
        //   name: widget.name,
        // );
        List<String> data = [
          ...sensorsData.accelerometerValues,
          ...sensorsData.userAccelerometerValues,
          // ...sensorsData.gyroscopeValues,
          // ...sensorsData.magnetometerValues,
        ];
        List<String> acc = sensorsData.accelerometerValues;
        for (int i = 0; i < data.length; i++) {
          _csvData.add(double.parse(data[i]));
        }

        for (int i = 0; i < acc.length; i++) {
          accel.add(double.parse(acc[i]));
        }

        if (_csvData.length >= 240) {
          var value = await ApiHandler.sendData(
            data: {
              "data": _csvData.sublist(0, 240),
              "accel": accel.sublist(0, 120),
            },
            url: widget.url,
          );
          setState(() {
            status = value.toString();
          });
          _csvData = [];
          accel = [];
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
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text("Predicted activity: $status"),
              ),
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
