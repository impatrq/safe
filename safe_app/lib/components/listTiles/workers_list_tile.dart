import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/components/customWidgets/worker_description_sheet.dart';

class WorkerListTile extends StatelessWidget {

  WorkerListTile({required this.imageURL, required this.workerName, required this.email, required this.address, required this.phoneNumber});

  final String imageURL;
  final String workerName;
  final String email;
  final String address;
  final String phoneNumber;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: (){
        Get.bottomSheet(
          WorkerDescriptionSheet(imageURL: imageURL, name: workerName, address: address, phoneNumber: phoneNumber, email: email),
          isScrollControlled: true,
        );
      },
      child: Column(
        children: [
          SizedBox(height: 10.0,),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              CircleAvatar(
                radius: 20.0,
                backgroundColor: Colors.transparent,
                backgroundImage: NetworkImage(imageURL),
              ),
              Expanded(
                child: Text(
                  workerName,
                  style: kLittleTitleTextStyle.copyWith(fontSize: 16.0),
                  textAlign: TextAlign.center,
                ),
              ),
              Icon(
                FontAwesomeIcons.ellipsisV,
                color: Color(0xFF333333),
              ),
            ],
          ),
          SizedBox(height: 10.0,),
          Divider(thickness: 1,),
        ],
      ),
    );
  }
}