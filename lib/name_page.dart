import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:orientation/homepage.dart';

class NameController extends StatefulWidget {
  const NameController({Key? key}) : super(key: key);

  @override
  State<NameController> createState() => _NameControllerState();
}

TextEditingController nameController = TextEditingController();

class _NameControllerState extends State<NameController> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              alignment: Alignment.bottomLeft,
              child: const Text('NameController'),
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: nameController,
              decoration: InputDecoration(
                border: InputBorder.none,
                filled: true,
                fillColor: Colors.grey.shade200,
                labelText: 'Name',
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pushReplacement(
                  CupertinoPageRoute(
                    builder: (context) => MyHomePage(
                      name: nameController.text,
                    ),
                  ),
                );
              },
              child: const Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}
