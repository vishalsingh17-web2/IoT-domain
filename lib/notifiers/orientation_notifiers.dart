import 'package:flutter/material.dart';
import 'package:orientation/notifiers/csv_notifier.dart';
import 'package:sensors_plus/sensors_plus.dart';

var sensor = Sensors();

class SensorsData extends ChangeNotifier {
  final Stream<AccelerometerEvent> _accelerometerEvent = sensor.accelerometerEvents;
  final Stream<GyroscopeEvent> _gyroscopeEvent = sensor.gyroscopeEvents;
  final Stream<MagnetometerEvent> _magnetometerEvent = sensor.magnetometerEvents;
  final Stream<UserAccelerometerEvent> _userAccelerometerEvent = sensor.userAccelerometerEvents;

  SensorsData() {
    startSensors();
  }

  List<String> accelerometerValues = [];
  List<String> userAccelerometerValues = [];
  List<String> gyroscopeValues = [];
  List<String> magnetometerValues = [];

  setAccelerometerValues(List<String> accelerometer) {
    accelerometerValues = accelerometer;
    notifyListeners();
  }

  setuserAccelerometerValues(List<String> userAccelerometer) {
    userAccelerometerValues = userAccelerometer;
    notifyListeners();
  }

  setGyroscopeValues(List<String> gyroscope) {
    gyroscopeValues = gyroscope;
    notifyListeners();
  }

  setMagnetometerValues(List<String> magnetometer) {
    magnetometerValues = magnetometer;
    notifyListeners();
  }

  startSensors() {
    _accelerometerEvent.listen(
      (AccelerometerEvent event) {
        setAccelerometerValues([event.x, event.y, event.z].map((e) => e.toStringAsFixed(2)).toList());
      },
    );
    _gyroscopeEvent.listen(
      (GyroscopeEvent event) {
        setGyroscopeValues([event.x, event.y, event.z].map((e) => e.toStringAsFixed(2)).toList());
      },
    );
    _userAccelerometerEvent.listen(
      (UserAccelerometerEvent event) {
        setuserAccelerometerValues([event.x, event.y, event.z].map((e) => e.toStringAsFixed(2)).toList());
      },
    );
    _magnetometerEvent.listen(
      (MagnetometerEvent event) {
        setMagnetometerValues([event.x, event.y, event.z].map((e) => e.toStringAsFixed(2)).toList());
      },
    );
    
    notifyListeners();
  }
}
