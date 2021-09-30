import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:safe_app/services/scrollable_row_controller.dart';

class ScrollableRow extends StatelessWidget {

  ScrollableRow({required this.items});

  final List<Widget> items;

  @override
  Widget build(BuildContext context) {
    return GetBuilder<ScrollableRowController>(
      init: ScrollableRowController(),
      builder: (controller) => Column(
        children: [
          SizedBox(height: 10.0,),
          Align(
            alignment: Alignment.centerLeft,
            child: Container(
              color: Colors.grey,
              width: controller.scrollRatio < 0 ? 0 : MediaQuery.of(context).size.width * controller.scrollRatio,
              height: 2.0,
            ),
          ),
          SizedBox(height: 10.0,),
          SingleChildScrollView(
            physics: BouncingScrollPhysics(),
            controller: controller.scrollController,
            scrollDirection: Axis.horizontal,
            child: Row(
              children: items,
            ),
          ),
        ],
      ),
    );
  }
}
