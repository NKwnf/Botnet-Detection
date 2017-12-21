/*
 * node.cc
 *
 */
#include "node.h"

Define_Module(Node);

void Node::initialize(){
    isSrc=this->par("isSrc");
    isDest=this->par("isDest").boolValue();
    isPrj1=this->getParentModule()->par("isPrj1");
    isPrj2=this->getParentModule()->par("isPrj2");
    isPrj3=this->getParentModule()->par("isPrj3");
    numNodes=this->getParentModule()->par("numNodes");
    txRate = par("txRate");
    pkLenBits = &par("pkLenBits");
    slotTime=this->par("slotTime").doubleValue();
    if(isSrc){
        scheduleAt(simTime(), new cMessage("",SRC_START));
    }
    FILE *pFile;
    pFile=fopen("senddata.txt","at");
    if(!pFile){
        perror("cannot open file");
        exit(1);
    }
    fprintf(pFile,"//////////////////////////////////////////");
    fputs("\n",pFile);
    fclose(pFile);
}

void Node::handleMessage(cMessage *msg){
    if(msg->isSelfMessage()){
        if(msg->getKind()==SRC_START){
            double rd=uniform(0,1);
            if(rd>0.6){
                sendBroadcastPacket();
            }else{
                sendReqPacket(getDestNode());
            }
            scheduleAt(simTime()+slotTime, new cMessage("",SRC_START));
        }
    }else{
        SrcPacket *pkt = check_and_cast<SrcPacket *>(msg);
        if(pkt->getKind()==REQ){
            if(isPrj1){
                sendResponse(pkt->getSrc());
            }else if(isPrj2){
                sendAckPacket(pkt->getSrc());
            }
            else{

            }
        }else if(pkt->getKind()==RES){
            sendAckPacket(pkt->getSrc());
        }else if(pkt->getKind()==ACK){
        }else if(pkt->getKind()==BROADCAST){
            if(isPrj3){

            }
            else{
                sendAckPacket(pkt->getSrc());
            }

        }
    }
}

int Node::getDestNode(){
    int dest=intuniform(0,numNodes-1);
    while(dest==this->getIndex()){
        dest=intuniform(0,numNodes-1);
    }
//    for(int i=1;i<=simulation.getLastModuleId();i++){
//        cModule *mod = (cModule *) simulation.getModule(i);
//        if(strcmp(mod->getName(), "node") == 0){
//            if(((Node*)mod)->isDest==true){
//                dest=((Node*)mod)->getIndex();
//                break;
//            }
//        }
//    }
    return dest;
}

void Node::sendReqPacket(int dest){
    Node *dstPtr=(Node*)(this->getParentModule()->getSubmodule("node", dest));
    SrcPacket *pk=new SrcPacket("req",REQ);
    pk->setBitLength(pkLenBits->longValue());
    pk->setSrc(this->getIndex());
    pk->setDest(dest);
    simtime_t duration = pk->getBitLength() / txRate;
    sendDirect(pk, 0, duration, dstPtr->gate("in"));
}

void Node::sendBroadcastPacket(){
    SrcPacket *pk=new SrcPacket("",BROADCAST);
    pk->setBitLength(pkLenBits->longValue());
    pk->setSrc(this->getIndex());
    pk->setDest(BROADCAST);
    simtime_t duration = pk->getBitLength() / txRate;
    for(int i=1;i<=simulation.getLastModuleId();i++){
        Node *mod = (Node *)simulation.getModule(i);
        if(mod->getIndex()!=this->getIndex()){
            sendDirect(pk->dup(), 0, duration, mod->gate("in"));
        }
    }
}

void Node::sendResponse(int dest){
    Node *dstPtr=(Node*)this->getParentModule()->getSubmodule("node", dest);
    SrcPacket *pk=new SrcPacket("response",RES);
    pk->setBitLength(pkLenBits->longValue());
    pk->setSrc(this->getIndex());
    pk->setDest(dest);
    simtime_t duration = pk->getBitLength() / txRate;
    double intervalTime=truncnormal(3, 1, 0);
    writeFile(this->getIndex(), intervalTime);
    sendDirect(pk, intervalTime, duration, dstPtr->gate("in"));
}
void Node::sendAckPacket(int dest){
    Node *dstPtr=(Node*)this->getParentModule()->getSubmodule("node", dest);
    SrcPacket *pk=new SrcPacket("ack",ACK);
    pk->setBitLength(pkLenBits->longValue());
    pk->setSrc(this->getIndex());
    pk->setDest(dest);
    simtime_t duration = pk->getBitLength() / txRate;
    double intervalTime=truncnormal(3, 1, 0);
    writeFile(this->getIndex(), intervalTime);
    sendDirect(pk, intervalTime, duration, dstPtr->gate("in"));
}

void Node::writeFile(int id,double interval){
    FILE *pFile;
    pFile=fopen("senddata.txt","at");
    if(!pFile){
        perror("cannot open file");
        exit(1);
    }
    fprintf(pFile,"%d -- %f",id,interval);
    fputs("\n",pFile);
    fclose(pFile);
}
