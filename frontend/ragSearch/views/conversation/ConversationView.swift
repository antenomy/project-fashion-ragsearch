//
//  AdminView.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//

import SwiftUI
import Combine

struct ConversationView : View {
    @ObservedObject var viewModel: SharedViewModel
    
    init(_ viewModel: SharedViewModel) {
        self.viewModel = viewModel
    }
    
    @State private var currentInput = ""
    
    @State private var allConversations: [Conversation] = [
        Conversation(
            chatMessages: ChatHistory(messages: []), systemRecommendations: []
        )
    ]
    
    @FocusState private var focusState: Bool
    @State private var hideInput = false
    @State private var showNewConversation = false
    
    @State private var awaitingResponse = false
    
    @State private var selectFavouritesOpen = false
    @State private var keyboardHeight: CGFloat = 0
    
    
    var body: some View {
        ZStack {
            VStack {
                ScrollView {
                    // Iterate over each conversation
                    ForEach(allConversations.indices, id: \.self) { indexA in
                        
                        
                        ForEach(allConversations[indexA].chatMessages.messages.indices, id: \.self) { indexB in
                            
                            TextBox(
                                message: allConversations[indexA].chatMessages.messages[indexB].content,
                                author_role: allConversations[indexA].chatMessages.messages[indexB].role
                            )
                        }
                        
                        ForEach(allConversations[indexA].systemRecommendations.indices, id: \.self) { indexC in
                            VStack {
                                TextBox(
                                    message: allConversations[indexA].systemRecommendations[indexC].message,
                                    author_role: "assistant"
                                )
                                
                                HStack(spacing: 8) {
                                    if allConversations[indexA].systemRecommendations[indexC].products.count >= 2 {
                                        ProductTile(
                                            allConversations[indexA].systemRecommendations[indexC].products[0],
                                            columnCount: 2
                                        )
                                        
                                        ProductTile(
                                            allConversations[indexA].systemRecommendations[indexC].products[1],
                                            columnCount: 2
                                        )
                                        
                                    } else if allConversations[indexA].systemRecommendations[indexC].products.count >= 1 {
                                        ProductTile(
                                            allConversations[indexA].systemRecommendations[indexC].products[1],
                                            columnCount: 1
                                        )
                                    }
                                }
                                .padding(.horizontal, 4)
                            }
                        }
                        .padding(.bottom, 16)
                    }
                    
                    if showNewConversation {
                        Button(action: {
                            showNewConversation = false
                            hideInput = false
                            focusState = true
                            currentInput = ""
                            allConversations.append(
                                Conversation(
                                    chatMessages: ChatHistory(messages: []), systemRecommendations: []
                                )
                            )
                            
                            //                        oldConversations.append(Conversation(chatMessages: currentChatHistory, systemRecommendations: systemChatReccomendations))
                            //                        currentChatHistory = ChatHistory(messages: [])
                            //                        systemChatReccomendations = []
                        }) {
                            CapsuleButton(
                                text: "New Conversation",
                                wideShape: false
                            )
                        }
                    }
                    
                    Color.clear
                        .padding(.vertical, 24)
                }
                .padding(.horizontal, 4)
                if !hideInput {
                    VStack {
//                        Spacer()
                        
                        Text("Hello, I am your smart fashion advisor!")
                            .basicText(size: 18)
                        
                        InputField($currentInput,
                                   $focusState,
                                   placeholderText: "Write what you are looking for today"
                        )
                        .padding(.horizontal, 16)
                        .padding(.bottom, keyboardHeight > 0 ? 0 : 32)
                        
                        // THIS HSTACK
                        HStack {
                            Menu {
                                Button(action:{ print("1") }) {
                                    Label("Add Photos", systemImage: "photo")
                                }
                                Button(action:{ print("2") }) {
                                    Label("Take Photo", systemImage: "camera")
                                }
                                Button(action:{ print("3") }) {
                                    Label("Add Files", systemImage: "folder")
                                }
                            } label: {
                                CircleButton(icon: "plus")
                            }
                            .padding(.leading, 16)
                            
                            Spacer()
                            
                            Button(action: {
                                withAnimation(.easeInOut(duration: (Const.animationTime))) {
                                    focusState = false
                                }
                                withAnimation(.easeInOut(duration: Const.animationTime)) {
                                    selectFavouritesOpen = true
                                    viewModel.showMenuSlider = false
                                }
                            }) {
                                CapsuleButton(
                                    text: "Select Similar Garment"
                                )
                            }
                            
                            Spacer()
                            
                            Button(action: {
                                withAnimation(.easeInOut(duration: Const.animationTime)) {
                                    focusState = false
                                    awaitingResponse = true
                                    hideInput = true
                                    
                                    // Done first so that it appears even if the thread is still processing
                                    if var currentConversation = allConversations.popLast() {
                                        currentConversation.chatMessages.messages.append(
                                            Message(role: "user", content: currentInput)
                                        )
                                        allConversations.append(currentConversation)
                                    }
                                    currentInput = ""
                                    
                                    Task {
                                        
                                        if let identifier = allConversations.last {
                                            let recieved_reccomendations = try await ItemHandler.reccomendationsFromPrompt(identifier.chatMessages)
                                            
                                            if var currentConversation = allConversations.popLast() {
                                                currentConversation.systemRecommendations = recieved_reccomendations ?? []
                                                allConversations.append(currentConversation)
                                            }
                                        }
                                        showNewConversation = true
                                        awaitingResponse = false
                                    }
                                }
                            }) {
                                CircleButton(icon: "arrow.up")
                            }
                            .padding(.trailing, 16)
                        }
                        .padding(.top, 2)
                        .padding(.bottom, 9)
                        .offset(y: keyboardHeight > 0 ? 0 : 100)
                        .opacity(keyboardHeight > 0 ? 1 : 0)
                        .animation(.easeInOut(duration: Const.animationTime), value: keyboardHeight)
                    }
                    .onReceive(Publishers.keyboardHeight) { height in
                        withAnimation {
                            self.keyboardHeight = height
                        }
                    }
                    .onSwipe(
                        up: {
                            print("up")
                            withAnimation(.easeInOut(duration: Const.animationTime)) {
                                focusState = true
                            }
                        },
                        down: {
                            print("down")
                            withAnimation(.easeInOut(duration: Const.animationTime)) {
                                focusState = false
                            }
                        })
                }
            }
            .frame(maxHeight: .infinity, alignment: .bottom)

            if selectFavouritesOpen {
                SelectFavourite(
//                   keepViewOpen: $selectFavouritesOpen
                    dismissAction: {
                        withAnimation(.easeInOut(duration: Const.animationTime)) {
                            selectFavouritesOpen = false
                            focusState = true
                            viewModel.showMenuSlider = true
                        }
                    }
                )
                .transition(.move(edge: .bottom))
                .animation(.easeInOut, value: selectFavouritesOpen)
            }
        }
        .onReceive(Publishers.keyboardHeight) { height in
            withAnimation(.easeInOut(duration: Const.animationTime * 0.5)) {
                self.keyboardHeight = height
            }
        }
    }
}

#Preview {
    ContentView(.conversation)
}
