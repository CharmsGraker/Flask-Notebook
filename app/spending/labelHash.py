import copy
import os
import pickle

import cv2


class LabelProjection:
    """
        实现spending整型映射至对应str，img path
    """

    def __init__(self, path_prefix, load_all=False):
        self.label_projection_prefix = path_prefix
        self.HASH_DIR = os.path.join(self.label_projection_prefix, 'hashTable')
        self.hashTable = [{}] * 2
        self.STR_TALBE = 0
        self.IMG_PATH_TALBE = 1
        self.ACCEPT_EXTENSION = ['jpg', 'jpeg', 'png']

        self.dump()

        self.inited = [False] * 2
        if load_all:
            self._loadLabelHashAll()

    def _loadLabelHashAll(self):
        self._loadStrTable()
        self._loadImgPathTable()

    def _loadImgPathTable(self):
        """
            加载持久化哈希表
        :return: label -> path projection
        """

        pkl_file = open(os.path.join(self.HASH_DIR, 'int2imgPath.pkl'), 'rb')
        self.hashTable[self.IMG_PATH_TALBE] = pickle.load(pkl_file)
        self.inited_ImgPath = True

    def _loadStrTable(self):
        pkl_file = open(os.path.join(self.HASH_DIR, 'int2str.pkl'), 'rb')
        self.hashTable[self.STR_TALBE] = pickle.load(pkl_file)
        self.inited_Str = True

    def dump(self):
        """
        持久化表
        :return:
        """
        STR_TABLE_PATH = os.path.join(self.HASH_DIR, 'int2str.pkl')
        IMG_TABLE_PATH = os.path.join(self.HASH_DIR, 'int2imgPath.pkl')

        if not os.path.exists(STR_TABLE_PATH):
            int2str_projection = {
                0: '普通',
                1: '娱乐',
                2: '学习',
                3: '日常'
            }

            with open(os.path.join(self.HASH_DIR, 'int2str.pkl'), 'wb') as f:
                pickle.dump(int2str_projection, f)

        if not os.path.exists(IMG_TABLE_PATH):
            # 我想的是，只存储名字映射关系，具体什么格式的图片可以再动态链接
            int2ImgName = {
                0: 'default',
                1: 'fun',
                2: 'study',
                3: 'ordinary'
            }
            FullImgMatchTable = self._ImgNameMatchToFile(int2ImgName)

            write_file = open(os.path.join(self.HASH_DIR, 'int2imgPath.pkl'), 'wb')

            pickle.dump(FullImgMatchTable, write_file)

    def _ImgNameMatchToFile(self, match_rule):
        """
        用于匹配完整的图片地址，之后进行持久化本地
        :param match_rule:
        :return:
        """

        to_be_matched = copy.deepcopy(match_rule)
        matched_table = copy.deepcopy(match_rule)

        for root, dirs, files in os.walk(self.label_projection_prefix):
            for file in files:
                # 包含扩展名
                # splitext只会分割最有一个点，那么可用于分割扩展名
                filename, file_ext = os.path.splitext(file)
                if file_ext not in file_ext in self.ACCEPT_EXTENSION:
                    continue
                for key, accept_value in matched_table.items():
                    if filename in accept_value:
                        matched_table[key] = os.path.join(self.label_projection_prefix, filename + file_ext)
                        del to_be_matched[key]
        print(to_be_matched)
        assert to_be_matched == {}
        to_be_matched = None
        return matched_table

    def getDefaultBanner(self, label):
        """
        哈希表存了各个标签对应的图片静态资源地址，可通过int类型标签直接取出
        :param label:
        :return:
        """

        if not self.inited[self.IMG_PATH_TALBE]:
            self._loadImgPathTable()
        imgPath_hash_table = self.hashTable[self.IMG_PATH_TALBE]

        banner_image_path = imgPath_hash_table.get(label, 'default')
        banner_image = cv2.imread(banner_image_path)

        banner_image_resize = cv2.resize(banner_image, (512, 512))
        return banner_image_resize

    def getStrLabel(self, label):
        if not self.inited[self.STR_TALBE]:
            self._loadStrTable()
        LabelStrProjection = self.hashTable[self.STR_TALBE].get(label)
        return LabelStrProjection

    def getInt2StrHashTable(self):
        if not self.inited[self.STR_TALBE]:
            self._loadStrTable()
        return self.hashTable[self.STR_TALBE]
