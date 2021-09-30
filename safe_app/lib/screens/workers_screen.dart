import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'dart:math';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/components/scaffolding/back_arrow_scaffold.dart';
import 'package:safe_app/components/listTiles/workers_list_tile.dart';
import 'package:safe_app/components/customWidgets/nfc_available_widget.dart';
import 'package:safe_app/services/safe_api_helper.dart';
import 'package:safe_app/services/safe_app_controller.dart';
import 'package:safe_app/services/spinning_controller.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/forms/worker_add_form.dart';


class WorkersScreen extends StatelessWidget {

  final SafeAppController _safeAppController = Get.find();

  final TextEditingController _workerSearchBarController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return BackArrowScaffold(
        body: GetBuilder<SafeAppController>(
          init: _safeAppController,
          builder: (controller) => Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Empleados',
                    style: kMediumTitleTextStyle,
                  ),
                  GetBuilder<SpinningController>(
                    init: SpinningController(),
                    builder: (spinningController) => Transform.rotate(
                      angle: (spinningController.animationController!.value * 360) * pi / 180,
                      child: IconButton(
                        onPressed: () async {
                          spinningController.startSpin();
                          await controller.updateWorkersList();
                          _workerSearchBarController.clear();
                          spinningController.stopSpin();
                        },
                        icon: Icon(
                          FontAwesomeIcons.syncAlt,
                          color: kLogoDarkBlueColor,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 10.0,),
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _workerSearchBarController,
                      onChanged: (newValue){},
                      decoration: InputDecoration(
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(5.0),
                          borderSide: BorderSide(
                              width: 1.0,
                              color: Colors.grey
                          ),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(5.0),
                          borderSide: BorderSide(
                              width: 2.0,
                              color: Colors.grey
                          ),
                        ),
                        hintText: 'Buscar por nombre / apellido',
                        contentPadding: EdgeInsets.all(12.0),
                        isCollapsed: true,
                      ),
                    ),
                  ),
                  SizedBox(width: 15.0,),
                  IconButton(
                    onPressed: () async {
                      // loadingController.toggleLoadingState();

                      if(_workerSearchBarController.text == ''){
                        controller.updateWorkersList();
                      } else {
                        controller.searchWorker(_workerSearchBarController.text);
                      }

                      // loadingController.toggleLoadingState();
                    },
                    icon: Icon(FontAwesomeIcons.search, color: kLogoDarkBlueColor,),
                  ),
                ],
              ),
              SizedBox(height: 10.0,),
              NFCAvailableWidget(
                availableWidget: Align(
                  alignment: Alignment.centerRight,
                  child: IconButton(
                    onPressed: (){
                      Get.bottomSheet(
                        WorkerBottomSheetAddForm(),
                      );
                    },
                    icon: Icon(
                      FontAwesomeIcons.plus,
                      color: kLogoDarkBlueColor,
                    ),
                  ),
                ),
              ),
              Divider(thickness: 2,),
              Text('Lista de Empleados', style: kLittleTitleTextStyle,),
              Divider(thickness: 2,),
              Expanded(
                child: Scrollbar(
                  radius: Radius.circular(10.0),
                  child: Padding(
                    padding: EdgeInsets.only(right: 5.0),
                    child: ListView.builder(
                      physics: BouncingScrollPhysics(),
                      itemBuilder: (context, index){
                        var worker = controller.data.workersList[index];
                        return WorkerListTile(
                          imageURL: worker.imagePath,
                          workerName: '${worker.firstName} ${worker.lastName}',
                          email: worker.email,
                          address: worker.address,
                          phoneNumber: worker.phoneNumber,
                        );
                      },
                      itemCount: controller.data.workersList.length,
                    ),
                  ),
                ),
              ),
            ],
          ),
        )
    );
  }
}