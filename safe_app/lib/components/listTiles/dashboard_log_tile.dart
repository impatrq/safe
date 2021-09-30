import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/utilities/constants.dart';

class DashboardLogTile extends StatelessWidget {

  DashboardLogTile({required this.imageURL, required this.workerName, required this.doorName, required this.allowed});

  final String imageURL;
  final String workerName;
  final String doorName;
  final bool allowed;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            CircleAvatar(
              backgroundColor: Colors.transparent,
              backgroundImage: NetworkImage(imageURL),
            ),
            SizedBox(width: 10.0,),
            Expanded(
              flex: 2,
                child: Text(
                  workerName,
                  style: kLittleTitleTextStyle.copyWith(fontSize: 16.0),
                  textAlign: TextAlign.center,
                )
            ),
            Expanded(
              flex: 3,
                child: Text(
                  '$doorName',
                  style: kLittleGreyTextStyle,
                  textAlign: TextAlign.center,
                )
            ),
            SizedBox(width: 10.0,),
            Icon(
              allowed ? FontAwesomeIcons.checkCircle : FontAwesomeIcons.timesCircle,
              color: allowed ? Colors.green : Colors.red,
            ),
          ],
        ),
        SizedBox(height: 15.0,),
      ],
    );
  }
}