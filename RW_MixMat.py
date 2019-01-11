#coding:utf-8

"""RW MixMat Bar_v1.1
    Update by Rookie
    Wechat：wyx769867389
    Email: 769867389@qq.com
    
    Description-US: RW_MixMat QBar
"""

import c4d
import copy
from c4d import documents, gui, bitmaps

#targ_obj = doc.GetActiveObject()  # Store target object


def main():
    # General
    doc = c4d.documents.GetActiveDocument()
    obj = doc.GetActiveObject()


    bc = c4d.BaseContainer()

    prefix = ("OR_")
    a = ("== ")
    b = (" ==")
    separator = (a + b + "&d&")

    # Icons
    ico_none = "&i1&"
    ico_RenderAllMats = "&i12253&"
    ico_DelUnusedMat = "&i12168&"

    ico_mix = "&i1033895&"
    ico_tags = "&i5616&"

    ico_node = "&i1033872&"

    ico_texman = "&i1035275&"

    ico_convert = "&i1029770&"

    # -- Build Menu  --

    entries = c4d.BaseContainer()
    # Node Editor Block
    entries.SetString(20, ico_none + a + "Node Editor" + b + "&d&")
    entries.SetString(21, ico_node + prefix + "Node Editor")
    # MixMat Block
    entries.SetString(000, ico_none + a + "Mix Mat" + b + "&d&")
    entries.SetString(11, ico_mix + prefix + "Duplicate Mix")
    entries.SetString(13, ico_mix + prefix + "Mix Mat")
    entries.SetString(14, ico_mix + prefix + "Rename Mix2")
    entries.SetString(15, ico_mix + prefix + "Select Father Mix")
    entries.SetString(16, ico_mix + prefix + "Select Mix Group")
    entries.SetString(17, ico_mix + prefix + "Select Top Mix")
    entries.SetString(18, ico_mix + prefix + "Switch Mix")
    # MatTool Block
    entries.SetString(200, ico_none + a + "Mat Tool" + b + "&d&")
    entries.SetString(201, ico_texman + prefix + "Tex Manager")

    entries.SetString(202, ico_convert + prefix + "Convert Mats")
    # MatHelp Block
    entries.SetString(100, ico_none + a + "MatHelp" + b + "&d&")
    entries.SetString(101, ico_tags + prefix + "Del Disabled MatTag")
    entries.SetString(102, ico_DelUnusedMat + prefix + "Del Unused Mat")
    entries.SetString(103, ico_RenderAllMats + prefix + " Render All Mats")


    # -- Build Objects --

    def DuplicateMix():
        mixlist = []
        matgroup = []
        matgroup2 = []
        templist = []
        matgroupnew = []
        matgroupnewmix = []
        i = 0
        j = 0
        matlist = doc.GetMaterials()

        SelMat = doc.GetActiveMaterial()

        for mat in matlist:
            if mat.GetType() == 1029622:  # MixMaterial type int
                mixlist.append(mat)

        # get all mixmaterials in doc

        while i < len(mixlist):
            for mat in mixlist:
                if SelMat == mat[c4d.MIXMATERIAL_TEXTURE1] or SelMat == mat[c4d.MIXMATERIAL_TEXTURE2]:
                    SelMat = mat
            i = i + 1

        if SelMat == None:
            gui.MessageDialog('Not Mixed!')

        # determine if selected material in any mix group

        c4d.CallCommand(300001026, 300001026)  # Deselect all mat

        while SelMat.GetType() == 1029622:
            SelMat.SetBit(c4d.BIT_ACTIVE)
            while SelMat[c4d.MIXMATERIAL_TEXTURE1].GetType() == 1029622:
                SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE1]
                SelMat.SetBit(c4d.BIT_ACTIVE)

            while SelMat[c4d.MIXMATERIAL_TEXTURE2].GetType() == 1029622:
                SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE2]
                SelMat.SetBit(c4d.BIT_ACTIVE)

            SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE1]

        mixlist2 = doc.GetActiveMaterials()

        # get all mixmaterials in selected mix group

        for mat in mixlist2:
            mat[c4d.MIXMATERIAL_TEXTURE1].SetBit(c4d.BIT_ACTIVE)
            mat[c4d.MIXMATERIAL_TEXTURE2].SetBit(c4d.BIT_ACTIVE)

        matgroup = doc.GetActiveMaterials()
        matgroup.reverse()

        # get all materials in seleceted mix group

        for mat in matgroup:
            matb = mat.GetClone()
            doc.InsertMaterial(matb)
            matgroupnew.append(matb)

        for mat in matgroupnew:
            if mat.GetType() == 1029622:
                matgroupnewmix.append(mat)

        matgroupnewmix.reverse()

        # dupilcate new materials

        c4d.CallCommand(300001026, 300001026)  # Deselect all mat

        while j < len(mixlist2):
            ind1 = matgroup.index(mixlist2[j][c4d.MIXMATERIAL_TEXTURE1])
            matgroupnewmix[j][c4d.MIXMATERIAL_TEXTURE1] = matgroupnew[ind1]

            ind2 = matgroup.index(mixlist2[j][c4d.MIXMATERIAL_TEXTURE2])
            matgroupnewmix[j][c4d.MIXMATERIAL_TEXTURE2] = matgroupnew[ind2]

            j = j + 1

        # insert sub materials for each mixmaterial

        c4d.EventAdd()



    def MixMat():
        doc.StartUndo()
        matlist = doc.GetActiveMaterials()
        if len(matlist) > 1:

            mixmat = c4d.BaseMaterial(1029622)

            doc.InsertMaterial(mixmat)
            doc.AddUndo(c4d.UNDOTYPE_NEW, mixmat)

            doc.AddUndo(c4d.UNDOTYPE_CHANGE, mixmat)
            mixmat[c4d.MIXMATERIAL_TEXTURE1] = matlist[0]

            mixmat[c4d.MIXMATERIAL_TEXTURE2] = matlist[1]

            doc.AddUndo(c4d.UNDOTYPE_CHANGE, mixmat)
            mixmat[c4d.ID_BASELIST_NAME] = matlist[0][c4d.ID_BASELIST_NAME] + '|' + matlist[1][c4d.ID_BASELIST_NAME]

        else:
            return

        c4d.EventAdd()
        doc.EndUndo()

    def RenameMix2():
        def CtrlKey():
            bc = c4d.BaseContainer()
            if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
                    return True
                else:
                    return False

        def RenameMixN():
            mixlist = []
            i = 0
            j = 2

            matlist = doc.GetMaterials()

            SelMat = doc.GetActiveMaterial()

            for mat in matlist:
                if mat.GetType() == 1029622:  # MixMaterial type int
                    mixlist.append(mat)

            # print mixlist
            while i < len(mixlist):
                for mat in mixlist:
                    if SelMat == mat[c4d.MIXMATERIAL_TEXTURE1] or SelMat == mat[c4d.MIXMATERIAL_TEXTURE2]:
                        SelMat = mat
                i = i + 1

            name = SelMat.GetName().split("|")[0]
            SelMat.SetName(name + "|●")

            while SelMat[c4d.MIXMATERIAL_TEXTURE1].GetType() == 1029622 or SelMat[
                c4d.MIXMATERIAL_TEXTURE2].GetType() == 1029622:
                if SelMat[c4d.MIXMATERIAL_TEXTURE1].GetType() == 1029622:
                    SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE1]
                else:
                    SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE2]
                SelMat.SetName(name + "|" + j * "●")
                j = j + 1

            c4d.EventAdd()

        def RenameMixP():
            mixlist = []
            mixlist2 = []
            i = 0
            j = 1

            matlist = doc.GetMaterials()

            SelMat = doc.GetActiveMaterial()

            for mat in matlist:
                if mat.GetType() == 1029622:  # MixMaterial type int
                    mixlist.append(mat)

            # print mixlist
            while i < len(mixlist):

                for mat in mixlist:
                    if SelMat == mat[c4d.MIXMATERIAL_TEXTURE1] or SelMat == mat[c4d.MIXMATERIAL_TEXTURE2]:
                        SelMat = mat
                i = i + 1

            name = SelMat.GetName().split("|")[0]
            top = SelMat
            SelMat2 = SelMat

            while SelMat2[c4d.MIXMATERIAL_TEXTURE1].GetType() == 1029622 or SelMat2[
                c4d.MIXMATERIAL_TEXTURE2].GetType() == 1029622:
                if SelMat2[c4d.MIXMATERIAL_TEXTURE1].GetType() == 1029622:
                    SelMat2 = SelMat2[c4d.MIXMATERIAL_TEXTURE1]
                    j = j + 1
                else:
                    SelMat2 = SelMat2[c4d.MIXMATERIAL_TEXTURE2]
                    j = j + 1

            top.SetName(name + "|" + j * "●")
            while SelMat[c4d.MIXMATERIAL_TEXTURE1].GetType() == 1029622 or SelMat[
                c4d.MIXMATERIAL_TEXTURE2].GetType() == 1029622:
                j = j - 1
                if SelMat[c4d.MIXMATERIAL_TEXTURE1].GetType() == 1029622:
                    SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE1]
                else:
                    SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE2]
                SelMat.SetName(name + "|" + j * "●")

            c4d.EventAdd()

        if __name__ == '__main__':
            if CtrlKey():
                RenameMixN()
            else:
                RenameMixP()

    def SelectFatherMix():
        mixlist = []
        i = 0
        matlist = doc.GetMaterials()

        SelMat = doc.GetActiveMaterial()

        for mat in matlist:
            if mat.GetType() == 1029622:  # MixMaterial type int
                mixlist.append(mat)

        # print mixlist
        for mat in mixlist:
            if SelMat == mat[c4d.MIXMATERIAL_TEXTURE1] or SelMat == mat[c4d.MIXMATERIAL_TEXTURE2]:
                SelMat = mat

        if SelMat == None:
            gui.MessageDialog('Not Mixed!')
        # print len(mixlist)
        c4d.CallCommand(300001026, 300001026)  # Deselect all mat

        SelMat.SetBit(c4d.BIT_ACTIVE)
        c4d.EventAdd()

    def SelectMixGroup():
        mixlist = []
        i = 0
        matlist = doc.GetMaterials()

        SelMat = doc.GetActiveMaterial()

        for mat in matlist:
            if mat.GetType() == 1029622:  # MixMaterial type int
                mixlist.append(mat)

        # print mixlist
        while i < len(mixlist):
            for mat in mixlist:
                if SelMat == mat[c4d.MIXMATERIAL_TEXTURE1] or SelMat == mat[c4d.MIXMATERIAL_TEXTURE2]:
                    SelMat = mat
            i = i + 1

        if SelMat == None:
            gui.MessageDialog('Not Mixed!')
        # print len(mixlist)
        c4d.CallCommand(300001026, 300001026)  # Deselect all mat

        # SelMat.SetBit(c4d.BIT_ACTIVE)
        while SelMat.GetType() == 1029622:
            SelMat.SetBit(c4d.BIT_ACTIVE)
            while SelMat[c4d.MIXMATERIAL_TEXTURE1].GetType() == 1029622:
                SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE1]
                SelMat.SetBit(c4d.BIT_ACTIVE)

            while SelMat[c4d.MIXMATERIAL_TEXTURE2].GetType() == 1029622:
                SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE2]
                SelMat.SetBit(c4d.BIT_ACTIVE)

            SelMat = SelMat[c4d.MIXMATERIAL_TEXTURE1]

        mixlist2 = doc.GetActiveMaterials()
        for mat in mixlist2:
            mat[c4d.MIXMATERIAL_TEXTURE1].SetBit(c4d.BIT_ACTIVE)
            mat[c4d.MIXMATERIAL_TEXTURE2].SetBit(c4d.BIT_ACTIVE)

        matgroup = doc.GetActiveMaterials()

    def SelectTopMix():
        mixlist = []
        i = 0
        matlist = doc.GetMaterials()

        SelMat = doc.GetActiveMaterial()

        for mat in matlist:
            if mat.GetType() == 1029622:  # MixMaterial type int
                mixlist.append(mat)

        # print mixlist
        while i < len(mixlist):
            for mat in mixlist:
                if SelMat == mat[c4d.MIXMATERIAL_TEXTURE1] or SelMat == mat[c4d.MIXMATERIAL_TEXTURE2]:
                    SelMat = mat
            i = i + 1

        if SelMat == None:
            gui.MessageDialog('Not Mixed!')
        # print len(mixlist)
        c4d.CallCommand(300001026, 300001026)  # Deselect all mat

        SelMat.SetBit(c4d.BIT_ACTIVE)
        c4d.EventAdd()

    def SwitchMix():
        mat = doc.GetActiveMaterial()
        mata = mat[c4d.MIXMATERIAL_TEXTURE1]
        matb = mat[c4d.MIXMATERIAL_TEXTURE2]
        mat[c4d.MIXMATERIAL_TEXTURE1] = matb
        mat[c4d.MIXMATERIAL_TEXTURE2] = mata

        c4d.EventAdd()

    def Tex():
        c4d.CallCommand(1035275)
        c4d.EventAdd()

    def Convert():
        active_mat = doc.GetActiveMaterial()
        if active_mat == None:
            gui.MessageDialog("Please select at least one Material")

        c4d.CallCommand(1029770, 1029770)
        c4d.EventAdd()

    def DelDisableTag():
        def nextObj(obj):
            if not obj: return
            elif obj.GetDown():
                return obj.GetDown()
            while obj.GetUp() and not obj.GetNext():
                obj = obj.GetUp()
            return obj.GetNext()

        def main():
            obj = doc.GetFirstObject()
            if not obj: return
            doc.StartUndo()
            while obj:
                for tag in obj.GetTags():
                    if tag.GetType() == 5616:
                        if tag[c4d.TEXTURETAG_MATERIAL] == None:
                            doc.AddUndo(c4d.UNDOTYPE_CHANGE,tag)
                            tag.Remove()
                obj = nextObj(obj)
        doc.EndUndo()
        c4d.EventAdd()

        if __name__=='__main__':
            main()

    def RenderAllMats():
        c4d.CallCommand(12253, 12253)  # Render All Material
        c4d.EventAdd()

    def Node():
        c4d.CallCommand(1033872)
        c4d.EventAdd()

    def DelUnusedMat():
        c4d.CallCommand(12168, 12168)  # Remove Unused Materials
        c4d.EventAdd()


    ########### -- User Input -- ###########

    result = gui.ShowPopupDialog(cd=None, bc=entries, x=c4d.MOUSEPOS, y=c4d.MOUSEPOS, flags=c4d.POPUP_RIGHT)

    if result == 11:
        DuplicateMix()
    elif result == 12:
        FolderMix()
    elif result == 13:
        MixMat()
    elif result == 14:
        RenameMix2()
    elif result == 15:
        SelectFatherMix()
    elif result == 16:
        SelectMixGroup()
    elif result == 17:
        SelectTopMix()
    elif result == 18:
        SwitchMix()

    elif result == 201:
        Tex()
    elif result == 202:
        Convert()

    elif result == 101:
        DelDisableTag()
    elif result == 102:
        DelUnusedMat()
    elif result == 103:
        RenderAllMats()


    else:
        return


if __name__ == '__main__':
    main()