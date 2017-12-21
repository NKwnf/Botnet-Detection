/*
 * node.h
 *
 *  Created on: 2017骞�2鏈�8鏃� *      Author: zzp
 */

#ifndef NODE_H_
#define NODE_H_

#include <omnetpp.h>
#include "sd_m.h"

#define REQ 1
#define RES 2
#define ACK 3
#define SRC_START 4

#define BROADCAST 1000
#define LIGHT_SPEED 299792458.0


class Node :public cSimpleModule{
protected:
  virtual void initialize() override;
  virtual void handleMessage(cMessage *msg) override;
  void sendReqPacket(int dest);
  void sendBroadcastPacket();
  void sendResponse(int dest);
  void sendAckPacket(int dest);
  int getDestNode();
  void writeFile(int id,double interval);
public:
  int dest;
  bool isSrc;
  bool isDest;
  bool isPrj1;
  bool isPrj2;
  bool isPrj3;
  int numNodes;
  double txRate;
  cPar *pkLenBits;
  double slotTime;
};



#endif /* NODE_H_ */
