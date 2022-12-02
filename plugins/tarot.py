# -*- coding: gbk -*-
import random
import os
from PIL import Image
import cv2
import numpy as np

tarot=[['���� (The Fool)','���㿪ʼ; �ö���; ��ī�سɹ�; ׷�����������; ð��; �����κ�; �����ҵ�����; ���ڳ���; ֱ��Ҫ����ä��; ����������; ����������ɣ; ������ʽ����������','������; ��עһ����ʧ��; ȱ�����θ�; ��ʧ; �Ÿ�վ����; ����; û��չ; û�ƻ�; �ߴ�·; ��Ϊ����; �ḡ������; ����������; �������İ���֮��','The Fool.jpg'],
  ['ħ��ʦ (The Magician)','�õĿ�ʼ; �߶�����; �з�չ��; �¼ƻ��ɹ�; �������ḻ���кõ���; �����鷢��; ӵ��Ĭ�����õİ���; �������˳���; ֵ��Ч�µĶ������','ʧ��; ����Ѷ�; ����ƽӹ; �б���թ��Σ��; ��������; ��������; û���ж���; ȱ��������; ����û�н�չ','The Magician.jpg'],
  ['Ů��˾ (The High Priestess)','֪�ԡ�������ж���; �߶��������ȼ�֮��; ǿ���ս����־; �侲��ͳ����; ѧ�ʡ��о��Ⱦ���������; ����������Ů��; ����ͼʽ�İ���; �������Ͻ������������; �䵭������','��֪��ȱ��������; �о�����; �����Ե�̬��; ���ҷ��; ����; ���; ��Ů����������ִ; �����䵭; ������������; û�н���ĵ���˼; ��ɫ����; ����','The High Priestess.jpg'],
  ['�ʵ� (The Emperor)','�Լ�ǿ����־����������³ɹ�; ��ԣ������; �����θ�; ���õĴ�������; ���쵼����; ���Ե�˼��; ��ֵ���; ���е�ר��ȴֵ������; �������˵�����; ���곤������','������; ��־����; �������; ��������ʵ; Ƿȱʵ������; ����������˷���; ��������; ��ִ; û�о��û���; û�кö���; ��������; ��ǿ�ĸ���','The Emperor.jpg'],
  ['�̻� (The Hierophant)','��������; �й�������; ����; ����˾����; ��ʤ�ι���; ӵ��һ���������; �ܻ�������Ľ���; �Ӵ��ڽ̵������; ���곤��������Ե; ��Ե; �������İ�; �н���Ե�Ļ���','û����; û�й�������; ������Ԯ; ���ܻ�ӭ�ĺ���; �����������ĵ���; ̫���¶�������; ����˽����޷��ɹ�; ������խ; �ò������˵��½������; �˴˹��ڹ���; Ե��ǳ��������','The Hierophant.jpg'],
  ['���� (The Lovers)','���˵Ľ��; ��ϣ���Ľ���; �й�ͬ���µĻ��; ���˺��������Ż; ���о���ǰ��֮·�ĺ�ʱ��; ��������Ͷ������; ������Ὣ����; �����ٿ˵�����; ����Ԥ��','����; ����; ��������̬��; �ۻ�����; û������ĳɹ�; �޷�����; ����; ����; Ѫ������; �������; ����; ��Į�İ�; ����; �ӱܰ���; ���ݵ�����','The Lovers.jpg'],
  ['ս�� (The Chariot)','ǰ����ʤ; ������Ϊǿ; ����; ���; �ڵ��������кóɼ�; ����; ��Ұ��; ���ٶ�ȡʤ; �п��ؾ���; ����ָ��Ȩ; սʤ����; ���ж���������; ������ʤ����','ʧ��; ɥʧս����־; ״̬����; ����; ���ӹ���Ϊʧ��֮��; ������Ȥ; Ч�ʲ���; �ʽ���ת����; �޷ܶ�����; ��ǿ�����ֽ���; ���ܾ�; ����ų��ʹ���鲻˳','The Chariot.jpg'],
  ['���� (Strength)','�������ӵľ���; �������ܻ�Ϊ���ܵ���־��; ȫ���Ը�; ͻ���ѹ�; ��ǿ�������Ŭ��; ��ս��֪Σ�յ�����; ���ص�����; ��ʢ�Ķ�־; ������ҵ�����; �˷����ѵ���ʵ����','���Ĳ�; ��ԥ����; ʵ������; ��������; Σ�յĶ�ע; ��ǿΪ֮���ʵ��䷴; ɥʧ����; ϲ����Ū����; ��������; �Դ��Ը�; ��������','Strength.jpg'],
  ['��ʿ (The Hermit)','������׿Խ����; ���ϵ�׷����߲�εĶ���; ˼������; �侲����; ������; �Ӵ�֪�����Ｊ; ���к��ĵĽ���; ��������н��гɹ�; ����; ׷�����ͼʽ�İ���; ���еİ���','һ��ͬ��; ����ͨ��; ��ר����������; ���־��䣬�޷�˳������; ����й©; ���ڹ�ִ�������˵����; �¶�; ����������; ��Թ�Լ�ƫ��������; �ḡ�İ���; ���ɰ���','The Hermit.jpg'],
  ['����֮�� (The Wheel of Fortune)','���ᵽ��; ���Ӧ��������; ����; ת����; ���벻��������; ��Ǩ����; �仯�ḻ; ��ʱ��; ���������; һ������; ���˵Ļ���; ���������','�ͳ���; ʱ��δ��; �����׳���; ʱ������; û��ͷ��; ��������; ������; �����; �ƻ�ͣ����Ҫ�ٵȴ�; ʧ��; ���ݵ�����; �״�ʧ����; �����ջ�; �����޷��־�','The Wheel of Fortune.jpg'],
  ['���� (Justice)','����; ���������; ���õľ����ϵ; ������������; ���º�����; �������ֹ���; Э����; ����С����������; ����һ�µĹ�������; �Գ�ʵ֮�Ĺ�������ؽ���; �˴��ܻ��Э��','������; ��ƽ��; ����������; ƫ��; ����Ϊ���Ĺ���; ƫ�������; ����������; ��������; �޷���ȫ; ��ƽ�����޷�ƽ��; �Ը�һ��; �����������¹۵�����; ƫ��','Justice.jpg'],
  ['������ (The Hanged Man)','���ܿ���; �޷�����; ������; ��ʧ���е�; ��ʹ��������л�ý�ѵ; ������; ��̰ͼ��ǰ����; ԡ������; �෽ѧϰ; ���׵İ�; ��֪���൫ȫ���Ը�','��ν������; �۶Ϲ�ͷ; ��ج�ˡ���������; ������Ϊ; ��Ŭ��; ���û������; ����������; �ܵ��ͷ�; �޳��İ�; ȱ����ͬ�ܶ��Ļ��','The Hanged Man.jpg'],
  ['���� (Death)','ʧ��; ����֮�ս���; �𺦼�������; ʧҵ; ��չͣ��; ����ֹͣ; Ϊʱ����; ͣ��״̬; ����������İ�ʾ; ζ�����������; ���ҵ�����; ������ֹ; �˴˼��к���ĺ蹵; ����','���������Ļ���; ���������; �ı�ӡ��; ����ת���ٳ���; �������; �漣�Ƶؿ���; ͻȻ�ı䷽��; �Ѿ����ĵ�������ת��; ն����˿�����³���','Death.jpg'],
  ['���� (Temperance)','������; ˳��; ����ƽ˳; ��������˳��; ����; �˴˽�����������; ƽ����Ҳ����Ҫ������; ƽ˳���ľ�; ����; �Ӻø�תΪ����; �','����; ÿ���Ƶ���ģ������Ĳ������õ�Ӱ��; ƣ��; �����ԵĹ���; ȱ����������; �½�; �˷�; ��Ҫ���� ����; ����Ǣ; �������϶Ȳ���','Temperance.jpg'],
  ['��ħ (The Devil)','������; ����; ��ħ��˽��; ������ϥ; �����ķ�²; �ķϵ�����; ��ծ����; ��ħ����; ҹ�ι���; ���ɸ��˵���; ����; ���ɿ��ܵ��ջ�; ˽������; �����ڸйٴ̼�֮��','�������; ���ڵĿ��ջ�ý��; ն��ǰԵ; Խ���ѹ�; ��ʱֹͣ; �ܾ��ջ�; ����˽��; �������ڲ�ʹ; ����   ʱ��; ���������Ӱ��޽��ӵ�����','The Devil.jpg'],
  ['�� (The Tower)','�����Ĵ��; ����; ���ײ���; ��������������������; ���벻��������; ����; ��ǣ��; ����Ĵ�䶯; �����; �澳; �Ʋ�; û��Ԥ����ͻȻ����; ����İ�; ����Է�','���ȵ�״̬; �ն������; ��ڧ; ��������; ������������; ������; ��ˮһս; ע����������; �򽾰��Դ󽫸�����ʹ�Ĵ���; ״������; ����; ����Σ��; �����Ԥ��','The Tower.jpg'],
  ['�ǳ� (The Star)','Ը�����; ǰ;����; ����ϣ����δ��; ���õ�����; ������; �󵨵Ļ���; ˮ׼���; �µĴ�����; ������; ����Ķ���; ���õ�����; ��������','���ۡ�ʧ��; �������; ȱ��������; �����쿪; ����ԸΥ; ʧ��; ���²�ϲ���Ĺ���; �ø���Զ; �������; �����ڴ��Ķ���; û �а�������; ��������; �ֻ�ʧ��','The Star.jpg'],
  ['���� (The Moon)','�����붯ҡ; ���в�ƽ��; ����; ��������; ��������; ���ض���; ��ƭ; ��ֹ; �����İ�; ���ǹ�ϵ','��Σ�յ�ƭ��������; ״����Ϊ��ת; ������; �Ƴ����; ʱ���ܽ��һ��; �۹�Ҫ��Զ; ���۵ȴ�; ���ڷ�������������Ч; ��ǰ��֪Σ��; ���������������Ѳ��ں�','The Moon.jpg'],
  ['̫�� (The Sun)','�ḻ��������; �޴�ĳɾ͸�; �˼ʹ�ϵ�ǳ���; ��������; ���ĳ��������������; һ���ܹ�ʵ�ֵ�Լ��; �ɻ��ڴ�; ��������','��������; ����ʧ��; ���ѵ���ȥ���˼ʹ�ϵ�Ķ�; �޷���������; �����µ���į; ���鲻˳ ��; ȡ���ļƻ�; ��������������','The Sun.jpg'],
  ['���� (Judgement)','�����ϲ��; ����; ����; �ĸ���; Σ�����; ����; ����; ո¶ͷ��; ����Ϣ; ����ʹ��; �ָ�����; ̹��; ���յİ�; �ٻ�; �����漣',' һ�ܲ���; ����; �븴�ջ��кܳ���ʱ��; �����ľ���; ��������; ��δ��ʼ�ͽ�����; ����Ϣ; ����; �޷�����; �����¿�ʼ��ȴ�ָֻ�ԭ״; ���롢����; ��������','Judgement.jpg'],
  ['���� (The World)','���; �ɹ�; ӵ�б�����־ҵ; ���Ŀ��; ��������; ��ʢ��; ������ȱ; �Ӵ���������������; �����׼; ���񿺷�; ���ֵĽ���; ģ������','δ���; �޷��ﵽ�ƻ��еĳɾ�; ��׼�������ʧ��; ��;�޷��ڽ���; ����ȫȼ��; һʱ��˳��; ����״̬; ��������; �����ɳ�; ���˹��õı��ַ�ʽ; �򲻳���� ʹ����ܴ�; ��ı; ̬�Ȳ���Բ��','The World.jpg']]
def tarotChoice(ints):
  if ints==0:
    tarots=random.choice(tarot)
    txt=tarots[0]+'\n'+'��λ'+'\n'+tarots[1]
    img='plugins\\TarotImages\\'+tarots[3]
    return txt,img
  if ints==1:
    tarots=random.choice(tarot)
    txt=tarots[0]+'\n'+'��λ'+'\n'+tarots[2]
    img='plugins\\TarotSide\\'+tarots[3]
    return txt,img





if __name__ == '__main__':
    tarotChoice(0)