import 'package:flutter/material.dart';
import 'package:orientation/homepage.dart';
import 'package:orientation/notifiers/orientation_notifiers.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:provider/provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  var permission = await Permission.storage.request();
  if (permission.isGranted) {
    runApp(const MyApp());
  } else {
    return runApp(const NotInitialized());
  }
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SensorsData()),
      ],
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Sensors Demo',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: const MyHomePage(),
      ),
    );
  }
}

class NotInitialized extends StatelessWidget {
  const NotInitialized({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SensorsData()),
      ],
      child: MaterialApp(
          debugShowCheckedModeBanner: false,
          title: 'Sensors Demo',
          theme: ThemeData(
            primarySwatch: Colors.blue,
          ),
          home: const Scaffold(
            body: Center(
              child: Text("Sensors not initialized"),
            ),
          )),
    );
  }
}
